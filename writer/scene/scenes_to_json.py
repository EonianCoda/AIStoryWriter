import writer.llm_editor
import writer.print_utils
import writer.config
import writer.chapter.chapter_gen_summary_check
import writer.prompts
from writer.interface.wrapper import Interface

def scenes_to_json(interface: Interface, logger, scenes: str):
    # This function converts the given scene list (from markdown format, to a specified JSON format).

    logger.log(f"Starting ChapterScenes->JSON", 2)
    message_history: list = []
    message_history.append(interface.build_system_query(writer.prompts.DEFAULT_SYSTEM_PROMPT))
    message_history.append(interface.build_user_query(writer.prompts.SCENES_TO_JSON.format(_Scenes=scenes)))

    _, scene_list = interface.safe_generate_json(logger, message_history, writer.config.CHECKER_MODEL)
    logger.log(f"Finished ChapterScenes->JSON ({len(scene_list)} Scenes Found)", 5)

    return scene_list