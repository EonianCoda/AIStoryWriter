import writer.llm_editor
import writer.print_utils
import writer.config
import writer.chapter.chapter_gen_summary_check
import writer.prompts


def ScenesToJSON(Interface, _Logger, _Scenes:str):

    # This function converts the given scene list (from markdown format, to a specified JSON format).

    _Logger.Log(f"Starting ChapterScenes->JSON", 2)
    MesssageHistory: list = []
    MesssageHistory.append(Interface.BuildSystemQuery(writer.prompts.DEFAULT_SYSTEM_PROMPT))
    MesssageHistory.append(Interface.BuildUserQuery(writer.prompts.SCENES_TO_JSON.format(_Scenes=_Scenes)))

    _, SceneList = Interface.SafeGenerateJSON(_Logger, MesssageHistory, writer.config.CHECKER_MODEL)
    _Logger.Log(f"Finished ChapterScenes->JSON ({len(SceneList)} Scenes Found)", 5)

    return SceneList
