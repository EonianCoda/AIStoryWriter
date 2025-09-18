import writer.llm_editor
import writer.print_utils
import writer.config
import writer.chapter.chapter_gen_summary_check
import writer.prompts
from writer.interface.wrapper import Interface

def scene_outline_to_scene(interface: Interface, logger, scene_outline: str, outline: str, base_context: str = ""):
    # Now we're finally going to go and write the scene provided.

    logger.log(f"Starting SceneOutline->Scene", 2)
    message_history: list = []
    message_history.append(interface.build_system_query(writer.prompts.DEFAULT_SYSTEM_PROMPT))
    message_history.append(interface.build_user_query(writer.prompts.SCENE_OUTLINE_TO_SCENE.format(_SceneOutline=scene_outline, _Outline=outline)))

    response = interface.safe_generate_text(logger, message_history, writer.config.CHAPTER_STAGE1_WRITER_MODEL, min_word_count=100)
    logger.log("Finished SceneOutline->Scene", 5)

    return interface.get_last_message_text(response)
