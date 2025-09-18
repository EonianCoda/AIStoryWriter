import writer.config
import dotenv
import inspect
import json
import os
import time
import random
import importlib
import subprocess
import sys
import re
from urllib.parse import parse_qs, urlparse

dotenv.load_dotenv()

class Interface:
    def __init__(
        self,
        models: list = [],
    ):
        """初始化 Interface，載入模型。"""
        self.clients: dict = {}
        self.history = []
        self.load_models(models)

    def _ensure_package_is_installed(self, package_name):
        """確保指定的 package 已安裝。"""
        try:
            importlib.import_module(package_name)
        except ImportError:
            print(f"Package {package_name} not found. Installing...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package_name]
            )

    def load_models(self, models: list):
        """載入所有指定模型。"""
        for model in models:
            if model in self.clients:
                continue
            else:
                provider, provider_model, model_host, model_options = (
                    self.get_model_and_provider(model)
                )
                print(f"DEBUG: Loading Model {provider_model} from {provider}@{model_host}")

                if provider == "ollama":
                    self._ensure_package_is_installed("ollama")
                    import ollama

                    ollama_host = model_host if model_host is not None else None

                    # 檢查模型是否已存在，若無則下載
                    try:
                        ollama.Client(host=ollama_host).show(provider_model)
                    except Exception as e:
                        print(
                            f"Model {provider_model} not found in Ollama models. Downloading..."
                        )
                        ollama_download_stream = ollama.Client(host=ollama_host).pull(
                            provider_model, stream=True
                        )
                        for chunk in ollama_download_stream:
                            if "completed" in chunk and "total" in chunk:
                                progress = chunk["completed"] / chunk["total"]
                                completed_size = chunk["completed"] / 1024**3
                                total_size = chunk["total"] / 1024**3
                                print(
                                    f"Downloading {provider_model}: {progress * 100:.2f}% ({completed_size:.3f}GB/{total_size:.3f}GB)",
                                    end="\r",
                                )
                            else:
                                print(f"{chunk['status']} {provider_model}", end="\r")
                        print("\n\n\n")

                    self.clients[model] = ollama.Client(host=ollama_host)
                    print(f"OLLAMA Host is '{ollama_host}'")

                elif provider == "google":
                    # 驗證 Google API Key
                    if (
                        not "GOOGLE_API_KEY" in os.environ
                        or os.environ["GOOGLE_API_KEY"] == ""
                    ):
                        raise Exception(
                            "GOOGLE_API_KEY not found in environment variables"
                        )
                    self._ensure_package_is_installed("google-generativeai")
                    import google.generativeai as genai

                    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
                    self.clients[model] = genai.GenerativeModel(
                        model_name=provider_model
                    )

                elif provider == "openai":
                    raise NotImplementedError("OpenAI API not supported")

                elif provider == "openrouter":
                    if (
                        not "OPENROUTER_API_KEY" in os.environ
                        or os.environ["OPENROUTER_API_KEY"] == ""
                    ):
                        raise Exception(
                            "OPENROUTER_API_KEY not found in environment variables"
                        )
                    from writer.Interface.OpenRouter import OpenRouter

                    self.clients[model] = OpenRouter(
                        api_key=os.environ["OPENROUTER_API_KEY"], model=provider_model
                    )

                elif provider == "Anthropic":
                    raise NotImplementedError("Anthropic API not supported")

                else:
                    print(f"Warning, ")
                    raise Exception(f"Model Provider {provider} for {model} not found")

    def safe_generate_text(
        self,
        logger,
        messages,
        model: str,
        seed_override: int = -1,
        format: str = None,
        min_word_count: int = 1
        ):
        """
        保證輸出不為空白。
        """

        # 移除空訊息
        for i in range(len(messages) - 1, 0, -1):
            if messages[i]["content"].strip() == "":
                del messages[i]

        new_msg = self.chat_and_stream_response(logger, messages, model, seed_override, format)

        while (self.get_last_message_text(new_msg).strip() == "") or (len(self.get_last_message_text(new_msg).split(" ")) < min_word_count):
            if self.get_last_message_text(new_msg).strip() == "":
                logger.log("SafeGenerateText: Generation Failed Due To Empty (Whitespace) Response, Reattempting Output", 7)
            elif (len(self.get_last_message_text(new_msg).split(" ")) < min_word_count):
                logger.log(f"SafeGenerateText: Generation Failed Due To Short Response ({len(self.get_last_message_text(new_msg).split(' '))}, min is {min_word_count}), Reattempting Output", 7)

            del messages[-1] # 移除失敗嘗試
            new_msg = self.chat_and_stream_response(logger, messages, model, random.randint(0, 99999), format)

        self.remove_think_tag_from_assistant_messages(new_msg)

        return new_msg

    def remove_think_tag_from_assistant_messages(self, messages):
        """移除 assistant 訊息中的 <think> 標籤。"""
        for msg in messages:
            if msg.get('role') == 'assistant' and 'content' in msg:
                msg['content'] = re.sub(r'<think>.*?</think>', '', msg['content'], flags=re.DOTALL)
    
    def safe_generate_json(self, logger, messages, model: str, seed_override: int = -1, required_attribs: list = []):
        """安全產生 JSON 格式回應，並檢查必要屬性。"""
        while True:
            response = self.safe_generate_text(logger, messages, model, seed_override, format="JSON")
            try:
                last_message = self.get_last_message_text(response)
                last_message = re.sub(r'^```json\s*', '', last_message)
                last_message = re.sub(r'\s*```$', '', last_message)
                json_response = json.loads(last_message)
                for attrib in required_attribs:
                    json_response[attrib]
                return response, json_response
            except Exception as e:
                logger.log(f"JSON Error during parsing: {e}", 7)
                del messages[-1]
                response = self.chat_and_stream_response(logger, messages, model, random.randint(0, 99999), format="JSON")

    def chat_and_stream_response(
        self,
        logger,
        messages,
        model: str = "llama3",
        seed_override: int = -1,
        format: str = None,
    ):
        """串流產生模型回應。"""
        provider, provider_model, model_host, model_options = self.get_model_and_provider(
            model
        )

        seed = writer.config.SEED if seed_override == -1 else seed_override

        # DEBUG 模式下印出訊息歷史
        if writer.config.DEBUG:
            print("--------- Message History START ---------")
            print("[")
            for message in messages:
                print(f"{message},\n----\n")
            print("]")
            print("--------- Message History END --------")

        start_generation = time.time()

        total_chars = len(str(messages))
        avg_chars_per_token = 5
        estimated_tokens = total_chars / avg_chars_per_token
        logger.log(
            f"Using Model '{provider_model}' from '{provider}@{model_host}' | (Est. ~{estimated_tokens}tok Context Length)",
            4,
        )

        if estimated_tokens > 24000:
            logger.log(
                f"Warning, Detected High Token Context Length of est. ~{estimated_tokens}tok",
                6,
            )

        if provider == "ollama":
            # 移除 host
            if "@" in provider_model:
                provider_model = provider_model.split("@")[0]

            valid_parameters = [
                "mirostat",
                "mirostat_eta",
                "mirostat_tau",
                "num_ctx",
                "repeat_last_n",
                "repeat_penalty",
                "temperature",
                "seed",
                "tfs_z",
                "num_predict",
                "top_k",
                "top_p",
            ]
            model_options = model_options if model_options is not None else {}

            for key in model_options:
                if key not in valid_parameters:
                    raise ValueError(f"Invalid parameter: {key}")

            if "num_ctx" not in model_options:
                model_options["num_ctx"] = writer.config.OLLAMA_CTX

            logger.log(f"Using Ollama Model Options: {model_options}", 4)

            if format == "json":
                model_options["format"] = "json"
                if "temperature" not in model_options:
                    model_options["temperature"] = 0
                logger.log("Using Ollama JSON Format", 4)

            stream = self.clients[model].chat(
                model=provider_model,
                messages=messages,
                stream=True,
                options=model_options,
            )
            max_retries = 3

            while True:
                try:
                    messages.append(self.stream_response(stream, provider))
                    break
                except Exception as e:
                    if max_retries > 0:
                        logger.log(
                            f"Exception During Generation '{e}', {max_retries} Retries Remaining",
                            7,
                        )
                        max_retries -= 1
                    else:
                        logger.log(
                            f"Max Retries Exceeded During Generation, Aborting!", 7
                        )
                        raise Exception(
                            "Generation Failed, Max Retires Exceeded, Aborting"
                        )

        elif provider == "google":
            from google.generativeai.types import (
                HarmCategory,
                HarmBlockThreshold,
            )

            # Google 需將 "content" 換成 "parts"
            messages = [{"role": m["role"], "parts": m["content"]} for m in messages]
            for m in messages:
                if "content" in m:
                    m["parts"] = m["content"]
                    del m["content"]
                if "role" in m and m["role"] == "assistant":
                    m["role"] = "model"
                if "role" in m and m["role"] == "system":
                    m["role"] = "user"

            max_retries = 3
            while True:
                try:
                    stream = self.clients[model].generate_content(
                        contents=messages,
                        stream=True,
                        safety_settings={
                            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                        },
                    )
                    messages.append(self.stream_response(stream, provider))
                    break
                except Exception as e:
                    if max_retries > 0:
                        logger.log(
                            f"Exception During Generation '{e}', {max_retries} Retries Remaining",
                            7,
                        )
                        max_retries -= 1
                    else:
                        logger.log(
                            f"Max Retries Exceeded During Generation, Aborting!", 7
                        )
                        raise Exception(
                            "Generation Failed, Max Retires Exceeded, Aborting"
                        )

            # 回復 "parts" 為 "content"，"model" 為 "assistant"
            for m in messages:
                if "parts" in m:
                    m["content"] = m["parts"]
                    del m["parts"]
                if "role" in m and m["role"] == "model":
                    m["role"] = "assistant"

        elif provider == "openai":
            raise NotImplementedError("OpenAI API not supported")

        elif provider == "openrouter":
            valid_parameters = [
                "max_token",
                "presence_penalty",
                "frequency_penalty",
                "repetition_penalty",
                "response_format",
                "temperature",
                "seed",
                "top_k",
                "top_p",
                "top_a",
                "min_p",
            ]
            model_options = model_options if model_options is not None else {}

            client = self.clients[model]
            client.set_params(**model_options)
            client.model = provider_model
            print(provider_model)

            response = client.chat(messages=messages, seed=seed)
            messages.append({"role": "assistant", "content": response})

        elif provider == "Anthropic":
            raise NotImplementedError("Anthropic API not supported")

        else:
            raise Exception(f"Model Provider {provider} for {model} not found")

        end_generation = time.time()
        logger.log(
            f"Generated Response in {round(end_generation - start_generation, 2)}s (~{round(estimated_tokens / (end_generation - start_generation), 2)}tok/s)",
            4,
        )
        # 若回應為空白則重試
        if messages[-1]["content"].strip() == "":
            logger.log("Model Returned Only Whitespace, Attempting Regeneration", 6)
            messages.append(
                self.build_user_query(
                    "Sorry, but you returned an empty string, please try again!"
                )
            )
            return self.chat_and_stream_response(logger, messages, model, seed_override)

        call_stack: str = ""
        for frame in inspect.stack()[1:]:
            call_stack += f"{frame.function}."
        call_stack = call_stack[:-1].replace("<module>", "Main")
        logger.SaveLangchain(call_stack, messages)
        return messages

    def stream_response(self, stream, provider: str):
        """串流取得模型回應。"""
        response: str = ""
        for chunk in stream:
            if provider == "ollama":
                chunk_text = chunk["message"]["content"]
            elif provider == "google":
                chunk_text = chunk.text
            else:
                raise ValueError(f"Unsupported provider: {provider}")

            response += chunk_text
            print(chunk_text, end="", flush=True)

        print("\n\n\n" if writer.config.DEBUG else "")
        return {"role": "assistant", "content": response}

    def build_user_query(self, query: str):
        return {"role": "user", "content": query}

    def build_system_query(self, query: str):
        return {"role": "system", "content": query}

    def build_assistant_query(self, query: str):
        return {"role": "assistant", "content": query}

    def get_last_message_text(self, messages: list):
        return messages[-1]["content"]

    def get_model_and_provider(self, model: str):
        """解析模型字串，取得 provider、model、host、options。"""
        # Format is `Provider://Model@Host?param1=value2&param2=value2`
        # default to ollama if no provider is specified
        if "://" in model:
            parsed = urlparse(model)
            print(parsed)
            provider = parsed.scheme

            if "@" in parsed.netloc:
                model_name, host = parsed.netloc.split("@")
            elif provider == "openrouter":
                model_name = f"{parsed.netloc}{parsed.path}"
                host = None
            elif "ollama" in model:
                if "@" in parsed.path:
                    model_name = parsed.netloc + parsed.path.split("@")[0]
                    host = parsed.path.split("@")[1]
                else:
                    model_name = parsed.netloc
                    host = "localhost:11434"
            else:
                model_name = parsed.netloc
                host = None
            query_params = parse_qs(parsed.query)

            # Flatten QueryParams
            for key in query_params:
                query_params[key] = float(query_params[key][0])

            return provider, model_name, host, query_params
        else:
            # legacy support for `Model` format
            return "ollama", model, "localhost:11434", None