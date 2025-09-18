"""Novel editing utilities."""

from typing import Any, List
from writer.interface.wrapper import Interface
import writer.print_utils
import writer.config
import writer.prompts
from writer.statistics import get_word_count

def edit_novel(
    interface: Interface,
    logger: Any,
    chapters: List[str],
    outline: str,
    num_chapters: int
) -> List[str]:
    """Edit the novel chapters."""
    edited_chapters = chapters

    for chapter_index in range(1, num_chapters + 1):

        novel_text: str = ""
        for chapter in edited_chapters:
            novel_text += chapter

        prompt: str = writer.prompts.CHAPTER_EDIT_PROMPT.format(
            _Chapter=edited_chapters[chapter_index], NovelText=novel_text, i=chapter_index
        )

        logger.log(
            f"Prompting LLM To Perform Chapter {chapter_index} Second Pass In-Place Edit", 5
        )
        messages = []
        messages.append(interface.build_user_query(prompt))
        messages = interface.safe_generate_text(
            logger, messages, writer.config.CHAPTER_WRITER_MODEL
        )
        logger.log(f"Finished Chapter {chapter_index} Second Pass In-Place Edit", 5)

        new_chapter = interface.get_last_message_text(messages)
        edited_chapters[chapter_index] = new_chapter
        chapter_word_count = get_word_count(new_chapter)
        logger.log(f"New Chapter Word Count: {chapter_word_count}", 3)

    return edited_chapters
