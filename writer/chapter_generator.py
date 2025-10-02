from typing import Any, List
from writer import interface, logger
from writer.config import (
    CHAPTER_STAGE1_WRITER_MODEL,
    CHAPTER_OUTLINE_WRITER_MODEL,
    CHECKER_MODEL,
    CHAPTER_STAGE2_WRITER_MODEL,
    CHAPTER_STAGE3_WRITER_MODEL,
    CHAPTER_STAGE4_WRITER_MODEL,
    CHAPTER_REVISION_WRITER_MODEL,
    CHAPTER_MAX_REVISIONS,
    CHAPTER_MIN_REVISIONS,
    CHAPTER_NO_REVISIONS,
    SCENE_GENERATION_PIPELINE,
    SEED,
)
from writer.prompts import load_prompt
from writer.logger import Logger
from writer.interface.wrapper import Interface
from writer.chapter.chapter_gen_summary_check import llm_summary_check
from writer.scene.chapter_by_scene import chapter_by_scene
from writer.generator import Generator

class ChapterGenerator(Generator):
    def generate_all_chapters(self, outline: str, num_chapters: int, extra_prompt_info: str):
        chapters = []
        for i in range(1, num_chapters + 1):
            chapter = self.generate_chapter(
                i,
                num_chapters,
                outline,
                chapters,
                extra_prompt_info,
            )
            # chapter = f"### Chapter {i}\n\n{chapter}"
            chapters.append(chapter)
            # chapter_word_count = get_word_count(chapter)
            # self.logger.log(f"Chapter Word Count: {chapter_word_count}", 2)

    def generate_chapter(self, chapter_idx: int, num_chapters: int, outline: str, chapters: List[str], extra_prompt_info: str) -> str:
        # 1. Prprocessing: Extract chapter outline from outline
        chapter_outline = self.extract_chapter_outline(outline, chapter_idx)

        # 2. Summarize last chapter
        if chapter_idx > 1:
           last_chapter_summary = self.summarize_last_chapter(chapter_idx, outline, chapters) 
    
    def chapter_by_scene(self, chapter_outline: str, outline: str):
        # This function calls all other scene-by-scene generation functions and creates a full chapter based on the new scene pipeline.

        self.logger.log(f"Starting Scene-By-Scene Chapter Generation Pipeline", 2)

        scenes_outline = self.chapter_outline_to_scene_outlines(chapter_outline, outline)

        scene_json_list = self.scenes_to_json(scenes_outline)

        # Now we iterate through each scene one at a time and write it, then add it to this rough chapter, which is then returned for further editing
        rough_chapter = ""
        for scene in scene_json_list:
            rough_chapter += self.scene_outline_to_scene(
                scene, outline
            )

        self.logger.log(f"Starting Scene-By-Scene Chapter Generation Pipeline", 2)

        return rough_chapter
    
    def scene_outline_to_scene(self, scene_outline: str, outline: str):
        # Now we're finally going to go and write the scene provided.

        self.logger.log(f"Starting SceneOutline->Scene", 2)
        message_history = [self.interface.build_system_query(self.novelist),
                           self.interface.build_user_query(self.load_prompt("scene_outline_to_scene").format(scene_outline=scene_outline), outline=outline)]

        messages = self.interface.generate_text(self.logger, message_history, CHAPTER_STAGE1_WRITER_MODEL, min_word_count=100)
        self.logger.log("Finished SceneOutline->Scene", 5)

        scene = self.interface.get_last_message_text(messages)  
        return scene

    def scenes_to_json(self, scenes: str) -> List[str]:
        # This function converts the given scene list (from markdown format, to a specified JSON format).

        self.logger.log(f"Starting ChapterScenes->JSON", 2)
        message_history: list = []
        message_history.append(self.interface.build_system_query(self.novelist))
        message_history.append(self.interface.build_user_query(self.load_prompt("scenes_to_json").format(scenes=scenes)))

        _, scene_list = self.interface.safe_generate_json(self.logger, message_history, CHECKER_MODEL)
        self.logger.log(f"Finished ChapterScenes->JSON ({len(scene_list)} Scenes Found)", 5)

        return scene_list
    
    def chapter_outline_to_scene_outlines(self, chapter_outline: str, outline: str):
        # We're now going to convert the chapter outline into a more detailed outline for each scene.
        # The scene by scene outline will be returned, JSONified, and then later converted into fully written scenes
        # These will then be concatenated into chapters and revised

        self.logger.log(f"Splitting Chapter Into Scenes", 2)
        message_history = [self.interface.build_system_query(self.novelist),
                           self.interface.build_user_query(self.load_prompt("chapter_outline_to_scene_outlines").format(chapter_content=chapter_outline, outline=outline))]

        messages = self.interface.generate_text(self.logger, message_history, CHAPTER_OUTLINE_WRITER_MODEL, min_word_count=100)
        self.logger.log("Finished Splitting Chapter Into Scenes", 5)

        scenes = self.interface.get_last_message_text(messages)
        return scenes

    def summarize_last_chapter(self, chapter_idx: int, outline: str, chapters: List[str]) -> None:
        self.logger.log(f"Creating Summary Of Last Chapter Info", 3)
        chapter_summary_messages = []
        chapter_summary_messages.append(
            self.interface.build_system_query(self.novelist)
        )
        chapter_summary_messages.append(
            self.interface.build_user_query(
                self.load_prompt("chapter_summary").format(
                    chapter_idx=chapter_idx,
                    outline=outline,
                    prev_chapter=chapters[-1],
                )
            )
        )
        chapter_summary_messages = self.interface.generate_text(
            self.logger,
            chapter_summary_messages,
            CHAPTER_STAGE1_WRITER_MODEL, 
            min_word_count=100
        ) 
        last_chapter_summary = self.interface.get_last_message_text(chapter_summary_messages)
        self.logger.log(f"Created Summary Of Last Chapter Info", 3)
        return last_chapter_summary
    
    def extract_chapter_outline(self, outline: str, chapter_idx):
        self.logger.log(f"Extracting Chapter Specific Outline", 4)

        messages = [self.novelist]  # Character prompt
        messages.append(
            self.get_chapter_prompt("chapter_outline_extraction").format(outline=outline, chapter_idx=chapter_idx)
        )
        messages = self.interface.generate_text(
            self.logger,
            messages,
            CHAPTER_STAGE1_WRITER_MODEL, min_word_count=120
        )
        chapter_outline = self.interface.get_last_message_text(messages)
        self.logger.log(f"Created Chapter Specific Outline", 4)
        return chapter_outline
        