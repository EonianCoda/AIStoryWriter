import writer.llm_editor
import writer.print_utils
import writer.config
import writer.chapter.chapter_gen_summary_check
import writer.prompts
from writer.interface.wrapper import Interface

def chapter_outline_to_scenes(interface: Interface, logger, this_chapter: str, outline: str, base_context: str = ""):
    # We're now going to convert the chapter outline into a more detailed outline for each scene.
    # The scene by scene outline will be returned, JSONified, and then later converted into fully written scenes
    # These will then be concatenated into chapters and revised

    logger.log(f"Splitting Chapter Into Scenes", 2)
    message_history: list = []
    message_history.append(interface.build_system_query(writer.prompts.DEFAULT_SYSTEM_PROMPT))
    message_history.append(interface.build_user_query(writer.prompts.CHAPTER_TO_SCENES.format(_ThisChapter=this_chapter, _Outline=outline)))

    response = interface.safe_generate_text(logger, message_history, writer.config.CHAPTER_OUTLINE_WRITER_MODEL, min_word_count=100)
    logger.log("Finished Splitting Chapter Into Scenes", 5)

    return interface.get_last_message_text(response)
