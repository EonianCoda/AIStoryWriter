import importlib

def load_prompt(feature, lang, name):
    """
    feature: 大功能資料夾，如 'summarization'
    lang: 語言，如 'zh_Hant'
    name: 檔名（不含 .py），如 'news'
    """
    module_path = f"{__name__}.{feature}.{lang}.{name.lower()}"
    mod = importlib.import_module(module_path)
    return getattr(mod, name.upper())

from .outline_prompts import (
    GET_IMPORTANT_BASE_PROMPT_INFO,
    STORY_ELEMENTS_PROMPT,
    CHAPTER_COUNT_PROMPT,
    INITIAL_OUTLINE_PROMPT,
    OUTLINE_REVISION_PROMPT,
    CHAPTER_OUTLINE_PROMPT,
    CRITIC_OUTLINE_PROMPT,
    OUTLINE_COMPLETE_PROMPT,
    SUMMARY_OUTLINE_INTRO,
    SUMMARY_OUTLINE_PROMPT,
)
from .chapter_prompts import (
    CHAPTER_GENERATION_INTRO,
    CHAPTER_HISTORY_INSERT,
    CHAPTER_GENERATION_PROMPT,
    CHAPTER_SUMMARY_INTRO,
    CHAPTER_SUMMARY_PROMPT,
    CHAPTER_GENERATION_STAGE1,
    CHAPTER_GENERATION_STAGE2,
    CHAPTER_GENERATION_STAGE3,
    CHAPTER_GENERATION_STAGE4,
    CHAPTER_REVISION,
    CHAPTER_COMPLETE_INTRO,
    CHAPTER_COMPLETE_PROMPT,
    CHAPTER_EDIT_PROMPT,
    CHAPTER_SCRUB_PROMPT,
    CHAPTER_TRANSLATE_PROMPT,
)
from .summary_prompts import (
    SUMMARY_CHECK_INTRO,
    SUMMARY_CHECK_PROMPT,
    SUMMARY_COMPARE_INTRO,
    SUMMARY_COMPARE_PROMPT,
)
from .translation_prompts import (
    TRANSLATE_PROMPT,
    CHAPTER_TRANSLATE_PROMPT,
)
from .stats_prompts import (
    STATS_PROMPT,
)
from .scene_prompts import (
    CHAPTER_TO_SCENES,
    SCENES_TO_JSON,
    SCENE_OUTLINE_TO_SCENE,
)

from .common_prompts import (
    JSON_PARSE_ERROR,
    CRITIC_CHAPTER_INTRO,
    CRITIC_CHAPTER_PROMPT,
    DEFAULT_SYSTEM_PROMPT,
)

from .character_system_prompts import (
    NOVELIST,
    NOVELISTV2,
    CRITIC,
    # editor,
    # critic,
    # translator,
    # reviewer,
)

from .translator import (
    CHINESE_TRANSLATOR
)