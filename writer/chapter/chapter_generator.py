"""Chapter generation utilities."""

from typing import Any, List
from writer.interface.wrapper import Interface

import writer.llm_editor
import writer.print_utils
import writer.config
import writer.chapter.chapter_gen_summary_check
import writer.prompts

import writer.scene.chapter_by_scene

def generate_chapter(
    interface: Interface,
    logger: Any,
    chapter_index: int,
    total_chapters: int,
    outline: str,
    chapters: List[str],
    outline_quality: Any,
    base_context: Any
) -> str:
    """Generate a chapter."""

    # Some important notes
    # We're going to remind the author model of the previous chapters here, so it knows what has been written before.

    #### Stage 0: Create base language chain
    logger.log(f"Creating Base Langchain For Chapter {chapter_index} Generation", 2)
    message_history: list = []
    message_history.append(
        interface.build_system_query(
            writer.prompts.CHAPTER_GENERATION_INTRO.format(
                _ChapterNum=chapter_index, _TotalChapters=total_chapters
            )
        )
    )

    context_history_insert: str = ""

    if len(chapters) > 0:

        chapter_superlist: str = ""
        for chapter in chapters:
            chapter_superlist += f"{chapter}\n"

        context_history_insert += writer.prompts.CHAPTER_HISTORY_INSERT.format(
            _Outline=outline, ChapterSuperlist=chapter_superlist
        )

    #
    # message_history.append(Interface.BuildUserQuery(f"""
    # Here is the novel so far.
    # """))
    # message_history.append(Interface.BuildUserQuery(ChapterSuperlist))
    # message_history.append(Interface.BuildSystemQuery("Make sure to pay attention to the content that has happened in these previous chapters. It's okay to deviate from the outline a little in order to ensure you continue the same story from previous chapters."))

    # Now, extract the this-chapter-outline segment
    logger.log(f"Extracting Chapter Specific Outline", 4)
    this_chapter_outline: str = ""
    chapter_segment_messages = []
    chapter_segment_messages.append(
        interface.build_system_query(writer.prompts.CHAPTER_GENERATION_INTRO)
    )
    chapter_segment_messages.append(
        interface.build_user_query(
            writer.prompts.CHAPTER_GENERATION_PROMPT.format(
                _Outline=outline, _ChapterNum=chapter_index
            )
        )
    )
    chapter_segment_messages = interface.safe_generate_text(
        logger,
        chapter_segment_messages,
        writer.config.CHAPTER_STAGE1_WRITER_MODEL, min_word_count=120
    )  # CHANGE THIS MODEL EVENTUALLY - BUT IT WORKS FOR NOW!!!
    this_chapter_outline: str = interface.get_last_message_text(chapter_segment_messages)
    logger.log(f"Created Chapter Specific Outline", 4)

    # Generate Summary of Last Chapter If Applicable
    formatted_last_chapter_summary: str = ""
    if len(chapters) > 0:
        logger.log(f"Creating Summary Of Last Chapter Info", 3)
        chapter_summary_messages = []
        chapter_summary_messages.append(
            interface.build_system_query(writer.prompts.CHAPTER_SUMMARY_INTRO)
        )
        chapter_summary_messages.append(
            interface.build_user_query(
                writer.prompts.CHAPTER_SUMMARY_PROMPT.format(
                    _ChapterNum=chapter_index,
                    _TotalChapters=total_chapters,
                    _Outline=outline,
                    _LastChapter=chapters[-1],
                )
            )
        )
        chapter_summary_messages = interface.safe_generate_text(
            logger,
            chapter_summary_messages,
            writer.config.CHAPTER_STAGE1_WRITER_MODEL, min_word_count=100
        )  # CHANGE THIS MODEL EVENTUALLY - BUT IT WORKS FOR NOW!!!
        formatted_last_chapter_summary: str = interface.get_last_message_text(
            chapter_summary_messages
        )
        logger.log(f"Created Summary Of Last Chapter Info", 3)

    detailed_chapter_outline: str = this_chapter_outline
    if formatted_last_chapter_summary != "":
        detailed_chapter_outline = this_chapter_outline

    logger.log(f"Done with base langchain setup", 2)


    # If scene generation disabled, use the normal initial plot generator
    stage1_chapter = ""
    if not writer.config.SCENE_GENERATION_PIPELINE:

        #### STAGE 1: Create Initial Plot
        iter_counter: int = 0
        feedback: str = ""
        while True:
            prompt = writer.prompts.CHAPTER_GENERATION_STAGE1.format(
                ContextHistoryInsert=context_history_insert,
                _ChapterNum=chapter_index,
                _TotalChapters=total_chapters,
                ThisChapterOutline=this_chapter_outline,
                FormattedLastChapterSummary=formatted_last_chapter_summary,
                Feedback=feedback,
                _BaseContext=base_context
            )

            # Generate Initial Chapter
            logger.log(
                f"Generating Initial Chapter (Stage 1: Plot) {chapter_index}/{total_chapters} (Iteration {iter_counter})",
                5,
            )
            messages = message_history.copy()
            messages.append(interface.build_user_query(prompt))

            messages = interface.safe_generate_text(
                logger,
                messages,
                writer.config.CHAPTER_STAGE1_WRITER_MODEL,
                seed_override=iter_counter + writer.config.SEED,
                min_word_count=100
            )
            iter_counter += 1
            stage1_chapter: str = interface.get_last_message_text(messages)
            logger.log(
                f"Finished Initial Generation For Initial Chapter (Stage 1: Plot)  {chapter_index}/{total_chapters}",
                5,
            )

            # Check if LLM did the work
            if iter_counter > writer.config.CHAPTER_MAX_REVISIONS:
                logger.log(
                    "Chapter Summary-Based Revision Seems Stuck - Forcefully Exiting", 7
                )
                break
            result, feedback = writer.chapter.chapter_gen_summary_check.llm_summary_check(
                interface, logger, detailed_chapter_outline, stage1_chapter
            )
            if result:
                logger.log(
                    f"Done Generating Initial Chapter (Stage 1: Plot)  {chapter_index}/{total_chapters}",
                    5,
                )
                break
    
    else:

        stage1_chapter = writer.scene.chapter_by_scene.ChapterByScene(interface, logger, this_chapter_outline, outline, base_context)


    #### STAGE 2: Add Character Development
    stage2_chapter = ""
    iter_counter: int = 0
    feedback: str = ""
    while True:
        prompt = writer.prompts.CHAPTER_GENERATION_STAGE2.format(
            ContextHistoryInsert=context_history_insert,
            _ChapterNum=chapter_index,
            _TotalChapters=total_chapters,
            ThisChapterOutline=this_chapter_outline,
            FormattedLastChapterSummary=formatted_last_chapter_summary,
            Stage1Chapter=stage1_chapter,
            Feedback=feedback,
            _BaseContext=base_context
        )

        # Generate Initial Chapter
        logger.log(
            f"Generating Initial Chapter (Stage 2: Character Development) {chapter_index}/{total_chapters} (Iteration {iter_counter})",
            5,
        )
        messages = message_history.copy()
        messages.append(interface.build_user_query(prompt))

        messages = interface.safe_generate_text(
            logger,
            messages,
            writer.config.CHAPTER_STAGE2_WRITER_MODEL,
            seed_override=iter_counter + writer.config.SEED,
            min_word_count=100
        )
        iter_counter += 1
        stage2_chapter: str = interface.get_last_message_text(messages)
        logger.log(
            f"Finished Initial Generation For Initial Chapter (Stage 2: Character Development)  {chapter_index}/{total_chapters}",
            5,
        )

        # Check if LLM did the work
        if iter_counter > writer.config.CHAPTER_MAX_REVISIONS:
            logger.log(
                "Chapter Summary-Based Revision Seems Stuck - Forcefully Exiting", 7
            )
            break
        result, feedback = writer.chapter.chapter_gen_summary_check.llm_summary_check(
            interface, logger, detailed_chapter_outline, stage2_chapter
        )
        if result:
            logger.log(
                f"Done Generating Initial Chapter (Stage 2: Character Development)  {chapter_index}/{total_chapters}",
                5,
            )
            break

    #### STAGE 3: Add Dialogue
    stage3_chapter = ""
    iter_counter: int = 0
    feedback: str = ""
    while True:
        prompt = writer.prompts.CHAPTER_GENERATION_STAGE3.format(
            ContextHistoryInsert=context_history_insert,
            _ChapterNum=chapter_index,
            _TotalChapters=total_chapters,
            ThisChapterOutline=this_chapter_outline,
            FormattedLastChapterSummary=formatted_last_chapter_summary,
            Stage2Chapter=stage2_chapter,
            Feedback=feedback,
            _BaseContext=base_context
        )
        # Generate Initial Chapter
        logger.log(
            f"Generating Initial Chapter (Stage 3: Dialogue) {chapter_index}/{total_chapters} (Iteration {iter_counter})",
            5,
        )
        messages = message_history.copy()
        messages.append(interface.build_user_query(prompt))

        messages = interface.safe_generate_text(
            logger,
            messages,
            writer.config.CHAPTER_STAGE3_WRITER_MODEL,
            seed_override=iter_counter + writer.config.SEED,
            min_word_count=100
        )
        iter_counter += 1
        stage3_chapter: str = interface.get_last_message_text(messages)
        logger.log(
            f"Finished Initial Generation For Initial Chapter (Stage 3: Dialogue)  {chapter_index}/{total_chapters}",
            5,
        )

        # Check if LLM did the work
        if iter_counter > writer.config.CHAPTER_MAX_REVISIONS:
            logger.log(
                "Chapter Summary-Based Revision Seems Stuck - Forcefully Exiting", 7
            )
            break
        result, feedback = writer.chapter.chapter_gen_summary_check.llm_summary_check(
            interface, logger, detailed_chapter_outline, stage3_chapter
        )
        if result:
            logger.log(
                f"Done Generating Initial Chapter (Stage 3: Dialogue)  {chapter_index}/{total_chapters}",
                5,
            )
            break

        #     #### STAGE 4: Final-Pre-Revision Edit Pass
        # Prompt = writer.prompts.CHAPTER_GENERATION_STAGE4.format(
        #    ContextHistoryInsert=ContextHistoryInsert,
        #     _ChapterNum=_ChapterNum,
        #     _TotalChapters=_TotalChapters,
        #     _Outline=_Outline,
        #     Stage3Chapter=Stage3Chapter,
        #     Feedback=Feedback,
        # )

    #     # Generate Initial Chapter
    #     _Logger.log(f"Generating Initial Chapter (Stage 4: Final Pass) {_ChapterNum}/{_TotalChapters}", 5)
    #     Messages = MesssageHistory.copy()
    #     Messages.append(Interface.BuildUserQuery(Prompt))

    #     Messages = Interface.SafeGenerateText(_Logger, Messages, writer.config.CHAPTER_STAGE4_WRITER_MODEL)
    #     Chapter:str = Interface.GetLastMessageText(Messages)
    #     _Logger.log(f"Done Generating Initial Chapter (Stage 4: Final Pass)  {_ChapterNum}/{_TotalChapters}", 5)
    chapter: str = stage3_chapter

    #### Stage 5: Revision Cycle
    if writer.config.CHAPTER_NO_REVISIONS:
        logger.log(f"Chapter Revision Disabled In Config, Exiting Now", 5)
        return chapter

    logger.log(
        f"Entering Feedback/Revision Loop (Stage 5) For Chapter {chapter_index}/{total_chapters}",
        4,
    )
    writing_history = message_history.copy()
    rating: int = 0
    iterations: int = 0
    while True:
        iterations += 1
        feedback = writer.llm_editor.get_feedback_on_chapter(
            interface, logger, chapter, outline
        )
        rating = writer.llm_editor.get_chapter_rating(interface, logger, chapter)

        if iterations > writer.config.CHAPTER_MAX_REVISIONS:
            break
        if (iterations > writer.config.CHAPTER_MIN_REVISIONS) and (rating is True):
            break
        chapter, writing_history = revise_chapter(
            interface, logger, chapter, feedback, writing_history
        )

    logger.log(
        f"Quality Standard Met, Exiting Feedback/Revision Loop (Stage 5) For Chapter {chapter_index}/{total_chapters}",
        4,
    )

    return chapter


def revise_chapter(interface: Interface, logger: Any, chapter, feedback, history: list = []):
    revision_prompt = writer.prompts.CHAPTER_REVISION.format(
        _Chapter=chapter, _Feedback=feedback
    )

    logger.log("Revising Chapter", 5)
    messages = history
    messages.append(interface.build_user_query(revision_prompt))
    messages = interface.safe_generate_text(
        logger, messages, writer.config.CHAPTER_REVISION_WRITER_MODEL,
        min_word_count=100
    )
    summary_text: str = interface.get_last_message_text(messages)
    logger.log("Done Revising Chapter", 5)

    return summary_text, messages
