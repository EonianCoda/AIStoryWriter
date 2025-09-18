"""Outline generation utilities."""

from typing import Any, Tuple, List
from writer.interface.wrapper import Interface
import writer.llm_editor
import writer.config
import writer.prompts

def generate_outline(
    interface: Interface,
    logger: Any,
    prompt: str,
    outline_quality: Any
) -> Tuple[str, Any, Any, Any]:
    """Generate the story outline."""

    prompt_info: str = writer.prompts.GET_IMPORTANT_BASE_PROMPT_INFO.format(
        _Prompt=prompt
    )

    logger.log("Extracting Important Base Context", 4)
    messages = [interface.build_user_query(prompt_info)]
    messages = interface.safe_generate_text(
        logger, messages, writer.config.INITIAL_OUTLINE_WRITER_MODEL
    )
    base_context: str = interface.get_last_message_text(messages)
    logger.log("Done Extracting Important Base Context", 4)


    story_elements: str = writer.outline.story_elements.GenerateStoryElements(
        interface, logger, prompt
    )


    outline_prompt: str = writer.prompts.INITIAL_OUTLINE_PROMPT.format(
        StoryElements=story_elements, _OutlinePrompt=prompt
    )


    logger.log("Generating Initial Outline", 4)
    messages = [interface.build_user_query(outline_prompt)]
    messages = interface.safe_generate_text(
        logger, messages, writer.config.INITIAL_OUTLINE_WRITER_MODEL, min_word_count=250
    )
    outline: str = interface.get_last_message_text(messages)
    logger.log("Done Generating Initial Outline", 4)

    logger.log("Entering Feedback/Revision Loop", 3)
    writing_history = messages
    rating: int = 0
    iterations: int = 0
    while True:
        iterations += 1
        feedback = writer.llm_editor.GetFeedbackOnOutline(interface, logger, outline)
        rating = writer.llm_editor.GetOutlineRating(interface, logger, outline)
        # Rating has been changed from a 0-100 int, to does it meet the standards (yes/no)?
        # Yes it has - the 0-100 int isn't actually good at all, LLM just returned a bunch of junk ratings

        if iterations > writer.config.OUTLINE_MAX_REVISIONS:
            break
        if (iterations > writer.config.OUTLINE_MIN_REVISIONS) and (rating is True):
            break

        outline, writing_history = revise_outline(interface, logger, outline, feedback, writing_history)

    logger.log("Quality Standard Met, Exiting Feedback/Revision Loop", 4)

    final_outline: str = f"""
{base_context}

{story_elements}

{outline}
    """

    return final_outline, story_elements, outline, base_context


def revise_outline(interface: Interface, logger: Any, outline, feedback, history: list = []):
    revision_prompt: str = writer.prompts.OUTLINE_REVISION_PROMPT.format(
        _Outline=outline, _Feedback=feedback
    )

    logger.log("Revising Outline", 2)
    messages = history
    messages.append(interface.build_user_query(revision_prompt))
    messages = interface.safe_generate_text(
        logger, messages, writer.config.INITIAL_OUTLINE_WRITER_MODEL, min_word_count=250
    )
    summary_text: str = interface.get_last_message_text(messages)
    logger.log("Done Revising Outline", 2)

    return summary_text, messages


def generate_per_chapter_outline(
    interface: Interface,
    logger: Any,
    chapter: int,
    outline: str,
    messages: List[Any]
) -> Tuple[str, List[Any]]:
    """Generate per-chapter outline."""

    revision_prompt: str = writer.prompts.CHAPTER_OUTLINE_PROMPT.format(
        _Chapter=chapter,
        _Outline=outline
    )
    logger.log("Generating Outline For Chapter " + str(chapter), 5)
    messages_list = messages
    messages_list.append(interface.build_user_query(revision_prompt))
    messages_list = interface.safe_generate_text(
        logger, messages_list, writer.config.CHAPTER_OUTLINE_WRITER_MODEL, min_word_count=50
    )
    summary_text: str = interface.get_last_message_text(messages_list)
    logger.log("Done Generating Outline For Chapter " + str(chapter), 5)

    return summary_text, messages_list