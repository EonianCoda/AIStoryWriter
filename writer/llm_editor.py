"""LLM Editor utilities."""

import json
from typing import Any
from writer.interface.wrapper import Interface
from writer.print_utils import Logger
from writer.prompts import (
    CRITIC_OUTLINE_INTRO,
    CRITIC_OUTLINE_PROMPT,
    OUTLINE_COMPLETE_INTRO,
    OUTLINE_COMPLETE_PROMPT,
    JSON_PARSE_ERROR,
    CRITIC_CHAPTER_INTRO,
    CRITIC_CHAPTER_PROMPT,
    CHAPTER_COMPLETE_INTRO,
    CHAPTER_COMPLETE_PROMPT,
)
from writer.config import REVISION_MODEL, EVAL_MODEL
import writer.prompts

def get_feedback_on_outline(interface: Interface, logger: Logger, outline: str) -> str:
    """Prompt LLM to critique outline."""
    history = []
    history.append(interface.build_system_query(CRITIC_OUTLINE_INTRO))
    starting_prompt = CRITIC_OUTLINE_PROMPT.format(_Outline=outline)
    logger.log("Prompting LLM To Critique Outline", 5)
    history.append(interface.build_user_query(starting_prompt))
    history = interface.safe_generate_text(
        logger, history, REVISION_MODEL, min_word_count=70
    )
    logger.log("Finished Getting Outline Feedback", 5)
    return interface.get_last_message_text(history)


def get_outline_rating(interface: Interface, logger: Logger, outline: str) -> bool:
    """Prompt LLM to get review JSON for outline."""
    history = []
    history.append(interface.build_system_query(OUTLINE_COMPLETE_INTRO))
    starting_prompt = OUTLINE_COMPLETE_PROMPT.format(_Outline=outline)
    logger.log("Prompting LLM To Get Review JSON", 5)
    history.append(interface.build_user_query(starting_prompt))
    history = interface.safe_generate_text(
        logger, history, EVAL_MODEL, format="json"
    )
    logger.log("Finished Getting Review JSON", 5)
    iters = 0
    while True:
        raw_response = interface.get_last_message_text(history)
        raw_response = raw_response.replace("`", "").replace("json", "")
        try:
            iters += 1
            rating = json.loads(raw_response)["IsComplete"]
            logger.log(f"Editor Determined IsComplete: {rating}", 5)
            return rating
        except Exception as e:
            if iters > 4:
                logger.log("Critical Error Parsing JSON", 7)
                return False
            logger.log("Error Parsing JSON Written By LLM, Asking For Edits", 7)
            edit_prompt = JSON_PARSE_ERROR.format(_Error=e)
            history.append(interface.build_user_query(edit_prompt))
            logger.log("Asking LLM TO Revise", 7)
            history = interface.safe_generate_text(
                logger, history, EVAL_MODEL, format="json"
            )
            logger.log("Done Asking LLM TO Revise JSON", 6)


def get_feedback_on_chapter(interface: Interface, logger: Logger, chapter: str, outline: str) -> str:
    """Prompt LLM to critique chapter."""
    history = []
    history.append(
        interface.build_system_query(
            CRITIC_CHAPTER_INTRO.format(_Chapter=chapter)
        )
    )
    starting_prompt = CRITIC_CHAPTER_PROMPT.format(
        _Chapter=chapter, _Outline=outline
    )
    logger.log("Prompting LLM To Critique Chapter", 5)
    history.append(interface.build_user_query(starting_prompt))
    messages = interface.safe_generate_text(
        logger, history, REVISION_MODEL
    )
    logger.log("Finished Getting Chapter Feedback", 5)
    return interface.get_last_message_text(messages)


def get_chapter_rating(interface: Interface, logger: Logger, chapter: str) -> bool:
    """Prompt LLM to get review JSON for chapter."""
    history = []
    history.append(interface.build_system_query(CHAPTER_COMPLETE_INTRO))
    starting_prompt = CHAPTER_COMPLETE_PROMPT.format(_Chapter=chapter)
    logger.log("Prompting LLM To Get Review JSON", 5)
    history.append(interface.build_user_query(starting_prompt))
    history = interface.safe_generate_text(
        logger, history, EVAL_MODEL
    )
    logger.log("Finished Getting Review JSON", 5)
    iters = 0
    while True:
        raw_response = interface.get_last_message_text(history)
        raw_response = raw_response.replace("`", "").replace("json", "")
        try:
            iters += 1
            rating = json.loads(raw_response)["IsComplete"]
            logger.log(f"Editor Determined IsComplete: {rating}", 5)
            return rating
        except Exception as e:
            if iters > 4:
                logger.log("Critical Error Parsing JSON", 7)
                return False
            logger.log("Error Parsing JSON Written By LLM, Asking For Edits", 7)
            edit_prompt = JSON_PARSE_ERROR.format(_Error=e)
            history.append(interface.build_user_query(edit_prompt))
            logger.log("Asking LLM TO Revise", 7)
            history = interface.safe_generate_text(
                logger, history, EVAL_MODEL
            )
            logger.log("Done Asking LLM TO Revise JSON", 6)
        RawResponse = RawResponse.replace("json", "")

        try:
            Iters += 1
            Rating = json.loads(RawResponse)["IsComplete"]
            logger.log(f"Editor Determined IsComplete: {Rating}", 5)
            return Rating
        except Exception as E:
            if Iters > 4:
                logger.log("Critical Error Parsing JSON", 7)
                return False

            logger.log("Error Parsing JSON Written By LLM, Asking For Edits", 7)
            EditPrompt: str = writer.prompts.JSON_PARSE_ERROR.format(_Error=E)
            History.append(interface.build_user_query(EditPrompt))
            logger.log("Asking LLM TO Revise", 7)
            History = interface.safe_generate_text(
                logger, History, writer.config.EVAL_MODEL
            )
            logger.log("Done Asking LLM TO Revise JSON", 6)
