
class ChapterGenerator:
    def __init__(self, interface, logger):
        self.interface = interface
        self.logger = logger

    def generate_chapter(self, chapter_title, chapter_outline, story_elements, base_context, chapter_number):
        prompt = f"Chapter {chapter_number}: {chapter_title}\n\nOutline: {chapter_outline}\n\nStory Elements: {story_elements}\n\nContext: {base_context}\n\nWrite the chapter in detail."
        response = self.interface.generate_text(prompt)
        self.logger.log(f"Generated Chapter {chapter_number}: {chapter_title}", 5)
        return response