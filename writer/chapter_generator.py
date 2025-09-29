from typing import Any, List
from writer import logger
from writer.config import (
    CHAPTER_STAGE1_WRITER_MODEL,
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
            # chapters.append(chapter)
            # chapter_word_count = get_word_count(chapter)
            # self.logger.log(f"Chapter Word Count: {chapter_word_count}", 2)
    
    def generate_chapter(self, chapter_title, chapter_outline, story_elements, base_context, chapter_number):
        # 1. Extract chapter outline from full outline
        chapter_outline = self.extract_chapter_outline(story_elements, chapter_number)

    
    def extract_chapter_outline(self, outline: str, chapter_idx):
        self.logger.log(f"Extracting Chapter Specific Outline", 4)
        
        messages = [self.novelist] # Character prompt
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
        