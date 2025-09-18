import writer.llm_editor
import writer.print_utils
import writer.config
import writer.chapter.chapter_gen_summary_check
import writer.prompts


def ChapterOutlineToScenes(Interface, _Logger, _ThisChapter:str, _Outline:str, _BaseContext: str = ""):

    # We're now going to convert the chapter outline into a more detailed outline for each scene.
    # The scene by scene outline will be returned, JSONified, and then later converted into fully written scenes
    # These will then be concatenated into chapters and revised


    _Logger.Log(f"Splitting Chapter Into Scenes", 2)
    MesssageHistory: list = []
    MesssageHistory.append(Interface.BuildSystemQuery(writer.prompts.DEFAULT_SYSTEM_PROMPT))
    MesssageHistory.append(Interface.BuildUserQuery(writer.prompts.CHAPTER_TO_SCENES.format(_ThisChapter=_ThisChapter, _Outline=_Outline)))

    Response = Interface.SafeGenerateText(_Logger, MesssageHistory, writer.config.CHAPTER_OUTLINE_WRITER_MODEL, _MinWordCount=100)
    _Logger.Log(f"Finished Splitting Chapter Into Scenes", 5)

    return Interface.GetLastMessageText(Response)
