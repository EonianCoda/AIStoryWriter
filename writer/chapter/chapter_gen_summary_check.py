"""Chapter summary check utilities."""

import json
from writer.interface.wrapper import Interface
from writer.llm_editor import (
    get_feedback_on_chapter,
    get_feedback_on_outline,
    get_chapter_rating,
    get_outline_rating,
)
from writer.print_utils import Logger
from writer.config import CHAPTER_STAGE1_WRITER_MODEL, REVISION_MODEL
from writer.prompts import (
    SUMMARY_CHECK_INTRO,
    SUMMARY_CHECK_PROMPT,
    SUMMARY_OUTLINE_INTRO,
    SUMMARY_OUTLINE_PROMPT,
    SUMMARY_COMPARE_INTRO,
    SUMMARY_COMPARE_PROMPT,
)


def llm_summary_check(interface: Interface, logger: Logger, ref_summary: str, work: str):
    """
    Generates a summary of the work provided, and compares that to the reference summary, asking if they answered the prompt correctly.
    """

    # LLM Length Check - Firstly, check if the length of the response was at least 100 words.
    if len(work.split(" ")) < 100:
        logger.log(
            "Previous response didn't meet the length requirement, so it probably tried to cheat around writing.",
            7,
        )
        return False, ""

    # Build Summariziation Langchain
    summary_langchain = []
    summary_langchain.append(
        interface.build_system_query(SUMMARY_CHECK_INTRO)
    )
    summary_langchain.append(
        interface.build_user_query(
            SUMMARY_CHECK_PROMPT.format(_Work=work)
        )
    )
    summary_langchain = interface.safe_generate_text(
        logger, summary_langchain, CHAPTER_STAGE1_WRITER_MODEL
    )  # CHANGE THIS MODEL EVENTUALLY - BUT IT WORKS FOR NOW!!!
    work_summary = interface.get_last_message_text(summary_langchain)

    # Now Summarize The Outline
    summary_langchain = []
    summary_langchain.append(
        interface.build_system_query(SUMMARY_OUTLINE_INTRO)
    )
    summary_langchain.append(
        interface.build_user_query(
            SUMMARY_OUTLINE_PROMPT.format(_RefSummary=ref_summary)
        )
    )
    summary_langchain = interface.safe_generate_text(
        logger, summary_langchain, CHAPTER_STAGE1_WRITER_MODEL
    )  # CHANGE THIS MODEL EVENTUALLY - BUT IT WORKS FOR NOW!!!
    outline_summary = interface.get_last_message_text(summary_langchain)

    # Now, generate a comparison JSON value.
    comparison_langchain = []
    comparison_langchain.append(
        interface.build_system_query(SUMMARY_COMPARE_INTRO)
    )
    comparison_langchain.append(
        interface.build_user_query(
            SUMMARY_COMPARE_PROMPT.format(
                WorkSummary=work_summary, OutlineSummary=outline_summary
            )
        )
    )
    comparison_langchain = interface.safe_generate_text(
        logger, comparison_langchain, REVISION_MODEL, format="json"
    )  # CHANGE THIS MODEL EVENTUALLY - BUT IT WORKS FOR NOW!!!

    iters = 0
    while True:

        raw_response = interface.get_last_message_text(comparison_langchain)
        raw_response = raw_response.replace("`", "").replace("json", "")

        try:
            iters += 1
            result_dict = json.loads(raw_response)
            return (
                result_dict["DidFollowOutline"],
                "### Extra Suggestions:\n" + result_dict["Suggestions"],
            )
        except Exception as e:
            if iters > 4:
                logger.log("Critical Error Parsing JSON", 7)
                return False, ""

            logger.log("Error Parsing JSON Written By LLM, Asking For Edits", 7)
            edit_prompt = (
                f"Please revise your JSON. It encountered the following error during parsing: {e}. Remember that your entire response is plugged directly into a JSON parser, so don't write **anything** except pure json."
            )
            comparison_langchain.append(interface.build_user_query(edit_prompt))
            logger.log("Asking LLM TO Revise", 7)
            comparison_langchain = interface.safe_generate_text(
                logger,
                comparison_langchain,
                REVISION_MODEL,
                format="json",
            )
            logger.log("Done Asking LLM TO Revise JSON", 6)
