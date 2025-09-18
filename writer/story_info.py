"""Story info utilities."""

from typing import Any, List, Dict
from writer.interface.wrapper import Interface
import writer.config
import json
import writer.prompts

def get_story_info(interface: Interface, logger: Any, messages: List[Any]) -> Dict[str, Any]:
    """Get story info such as title, summary, tags."""

    prompt: str = writer.prompts.STATS_PROMPT

    logger.log("Prompting LLM To Generate Stats", 5)
    messages_list = messages
    messages_list.append(interface.build_user_query(prompt))
    messages_list = interface.safe_generate_text(
        logger, messages_list, writer.config.INFO_MODEL, format="json"
    )
    logger.log("Finished Getting Stats Feedback", 5)

    iters: int = 0
    while True:

        raw_response = interface.get_last_message_text(messages_list)
        raw_response = raw_response.replace("`", "")
        raw_response = raw_response.replace("json", "")

        try:
            iters += 1
            dict_obj = json.loads(raw_response)
            return dict_obj
        except Exception as e:
            if iters > 4:
                logger.log("Critical Error Parsing JSON", 7)
                return {}
            logger.log("Error Parsing JSON Written By LLM, Asking For Edits", 7)
            edit_prompt: str = (
                f"Please revise your JSON. It encountered the following error during parsing: {e}. Remember that your entire response is plugged directly into a JSON parser, so don't write **anything** except pure json."
            )
            messages_list.append(interface.build_user_query(edit_prompt))
            logger.log("Asking LLM TO Revise", 7)
            messages_list = interface.safe_generate_text(
                logger, messages_list, writer.config.INFO_MODEL, format="json"
            )
            logger.log("Done Asking LLM TO Revise JSON", 6)
