"""Novel scrubbing utilities."""

from typing import Any, List

from writer.logger import Logger
from writer.prompts import CHAPTER_SCRUB_PROMPT
from writer.config import SCRUB_MODEL
from writer.statistics import get_word_count
from writer.interface.wrapper import Interface

def scrub_novel(
    interface: Interface,
    logger: Any,
    chapters: List[str],
    num_chapters: int
) -> List[str]:
    """Scrub the novel chapters."""

    edited_chapters = chapters

    for i in range(num_chapters):

        prompt: str = CHAPTER_SCRUB_PROMPT.format(
            _Chapter=edited_chapters[i]
        )
        logger.log(f"Prompting LLM To Perform Chapter {i+1} Scrubbing Edit", 5)
        messages = []
        messages.append(interface.build_user_query(prompt))
        messages = interface.generate_text(
            logger, messages, SCRUB_MODEL
        )
        logger.log(f"Finished Chapter {i+1} Scrubbing Edit", 5)

        new_chapter = interface.get_last_message_text(messages)
        edited_chapters[i] = new_chapter
        chapter_word_count = get_word_count(new_chapter)
        logger.log(f"Scrubbed Chapter Word Count: {chapter_word_count}", 3)

    return edited_chapters
