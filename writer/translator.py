"""Translation utilities."""

from typing import Any, List
from writer.interface.wrapper import Interface

import writer.config
import writer.prompts
import writer.statistics


def translate_prompt(
    interface: Interface,
    logger: Any,
    prompt: str,
    language: str = "French",
) -> str:
    """Translate the input prompt to the specified language."""

    formatted_prompt: str = writer.prompts.TRANSLATE_PROMPT.format(
        _Prompt=prompt, _Language=language
    )
    logger.log("Prompting LLM To Translate User Prompt", 5)
    messages = []
    messages.append(interface.build_user_query(formatted_prompt))
    messages = interface.safe_generate_text(
        logger, messages, writer.config.TRANSLATOR_MODEL, min_word_count=50
    )
    logger.log("Finished Prompt Translation", 5)

    return interface.get_last_message_text(messages)


def translate_novel(
    interface: Interface,
    logger: Any,
    chapters: List[str],
    num_chapters: int,
    language: str = "French",
) -> List[str]:
    """Translate the novel chapters to the specified language."""

    edited_chapters = chapters

    for chapter_index in range(num_chapters):

        formatted_prompt: str = writer.prompts.CHAPTER_TRANSLATE_PROMPT.format(
            _Chapter=edited_chapters[chapter_index], _Language=language
        )
        logger.log(f"Prompting LLM To Perform Chapter {chapter_index+1} Translation", 5)
        messages = []
        messages.append(interface.build_user_query(formatted_prompt))
        messages = interface.safe_generate_text(
            logger, messages, writer.config.TRANSLATOR_MODEL
        )
        logger.log(f"Finished Chapter {chapter_index+1} Translation", 5)

        new_chapter = interface.get_last_message_text(messages)
        edited_chapters[chapter_index] = new_chapter
        chapter_word_count = writer.statistics.get_word_count(new_chapter)
        logger.log(f"Translation Chapter Word Count: {chapter_word_count}", 3)

    return edited_chapters
