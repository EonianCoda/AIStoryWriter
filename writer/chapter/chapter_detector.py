"""Chapter detection utilities."""

from typing import Any

import writer.config
import writer.prompts
import json
from writer.interface.wrapper import Interface

def llm_count_chapters(interface: Interface, logger: Any, message_text: str) -> int:
    """Count chapters using LLM."""

    prompt = writer.prompts.CHAPTER_COUNT_PROMPT.format(_Summary=message_text)

    logger.log("Prompting LLM To Get ChapterCount JSON", 5)
    messages = []
    messages.append(interface.build_user_query(prompt))
    messages = interface.safe_generate_text(
        logger, messages, writer.config.EVAL_MODEL, _Format="json"
    )
    logger.log("Finished Getting ChapterCount JSON", 5)

    iters: int = 0

    while True:

        raw_response = interface.get_last_message_text(messages)
        raw_response = raw_response.replace("`", "")
        raw_response = raw_response.replace("json", "")

        try:
            iters += 1
            total_chapters = json.loads(raw_response)["TotalChapters"]
            logger.log("Got Total Chapter Count At {TotalChapters}", 5)
            return total_chapters
        except Exception as e:
            if iters > 4:
                logger.log("Critical Error Parsing JSON", 7)
                return -1
            logger.log("Error Parsing JSON Written By LLM, Asking For Edits", 7)
            edit_prompt: str = (
                f"Please revise your JSON. It encountered the following error during parsing: {e}. Remember that your entire response is plugged directly into a JSON parser, so don't write **anything** except pure json."
            )
            messages.append(interface.build_user_query(edit_prompt))
            logger.log("Asking LLM TO Revise", 7)
            messages = interface.safe_generate_text(
                logger, messages, writer.config.EVAL_MODEL, _Format="json"
            )
            logger.log("Done Asking LLM TO Revise JSON", 6)
