"""Outline generation utilities."""
import json
from typing import Any, Tuple, List
from writer.config import (
    INITIAL_OUTLINE_WRITER_MODEL,
    OUTLINE_MAX_REVISIONS,
    OUTLINE_MIN_REVISIONS,
    CHAPTER_OUTLINE_WRITER_MODEL,
)
from writer.config import REVISION_MODEL, EVAL_MODEL
from writer.generator import Generator

class OutlineGenerator(Generator):
    def generate_outline(self, user_story_prompt: str) -> Tuple[str, Any, Any, Any]:
        """Generate the story outline."""

        # 1. Extract Important Base Context
        self.logger.log("Extracting Important Base Context", 4)
        messages = [self.interface.build_system_query(self.novelist),
                    self.interface.build_user_query(self.get_outline_prompt("extra_prompt_info_generation").format(user_story_prompt=user_story_prompt))]
        messages = self.interface.generate_text(
            self.logger, messages, INITIAL_OUTLINE_WRITER_MODEL
        )
        extra_prompt_info = self.interface.get_last_message_text(messages)
        self.logger.log("Done Extracting Important Base Context", 4)

        # 2. Generate Story Elements
        story_elements = self.generate_story_elements(user_story_prompt)
        
        # 3. Generate Initial Outline
        rough_outline, writing_history = self.generate_initial_outline(user_story_prompt, story_elements)
        
        self.logger.log("Entering Feedback/Revision Loop", 3)
        rating: int| bool = 0
        iterations: int = 0
        
        while True:
            iterations += 1
            # 4. Get Feedback on Outline
            feedback = self.get_feedback_on_outline(rough_outline)
            # 4.5 Get Rating on Outline
            rating = self.get_outline_rating(rough_outline)
            # Currently get_outline_rating returns a bool - does it meet the standards (yes/no)?
            #TODO Future - could return a 0-100 int rating again if needed
                # Rating has been changed from a 0-100 int, to does it meet the standards (yes/no)?
                # Yes it has - the 0-100 int isn't actually good at all, LLM just returned a bunch of junk ratings

            # Check if retry iterations exceeded max, or if rating is good enough and min iterations met
            if (iterations > OUTLINE_MAX_REVISIONS) or (rating is True and iterations >= OUTLINE_MIN_REVISIONS):
                break
            
            # 5. Revise Outline (if rating not good enough)
            rough_outline, writing_history = self.revise_outline(rough_outline, feedback, writing_history)

        self.logger.log("Quality Standard Met, Exiting Feedback/Revision Loop", 4)

        outline: str = f"""{extra_prompt_info}
        {story_elements}
        {rough_outline}"""  
        return outline, story_elements, rough_outline, extra_prompt_info

    def generate_story_elements(self, user_story_prompt: str):
        # Generate Initial Story Elements
        self.logger.log("Generating Main Story Elements", 4)

        story_elements_prompt = self.get_outline_prompt("story_elements").format(user_story_prompt=user_story_prompt)

        messages = [self.interface.build_system_query(self.novelist),
                    self.interface.build_user_query(story_elements_prompt)]
        messages = self.interface.generate_text(
            self.logger, messages, INITIAL_OUTLINE_WRITER_MODEL, min_word_count=150
        )
        elements = self.interface.get_last_message_text(messages)
        self.logger.log("Done Generating Main Story Elements", 4)

        return elements

    def generate_initial_outline(self, 
                         user_story_prompt: str,
                         story_elements: str):
        outline_prompt = self.get_outline_prompt("initial_outline").format(story_elements=story_elements, 
                                                                    outline_prompt=user_story_prompt)

        self.logger.log("Generating Initial Outline", 4)
        messages = [self.interface.build_system_query(self.novelist),
                    self.interface.build_user_query(outline_prompt)]
        messages = self.interface.generate_text(
            self.logger, messages, INITIAL_OUTLINE_WRITER_MODEL, min_word_count=250
        )
        outline = self.interface.get_last_message_text(messages)
        self.logger.log("Done Generating Initial Outline", 4)
        
        return outline, messages

    def get_feedback_on_outline(self, outline: str) -> str:
        """Prompt LLM to critique outline."""
        history = [self.interface.build_system_query(self.critic)] # Character
        critic_outline_prompt = self.get_outline_prompt("critic_outline").format(outline=outline)

        self.logger.log("Prompting LLM To Critique Outline", 5)
        history.append(self.interface.build_user_query(critic_outline_prompt))
        history = self.interface.generate_text(
            self.logger, history, REVISION_MODEL, min_word_count=70
        )
        self.logger.log("Finished Getting Outline Feedback", 5)
        
        return self.interface.get_last_message_text(history)

    def get_outline_rating(self, outline: str) -> bool:
        """Prompt LLM to get review JSON for outline."""
        
        history = []
        history.append(self.interface.build_system_query(self.get_character_prompt("critic"))) # Character
        starting_prompt = self.get_outline_prompt("outline_complete").format(outline=outline)
        self.logger.log("Prompting LLM To Get Review JSON", 5)
        history.append(self.interface.build_user_query(starting_prompt))
        history = self.interface.generate_text(
            self.logger, history, EVAL_MODEL, format="json"
        )
        self.logger.log("Finished Getting Review JSON", 5)
        
        # Try to parse the JSON response, if it fails ask the LLM to fix it
        iters = 0
        while True:
            raw_response = self.interface.get_last_message_text(history)
            raw_response = raw_response.replace("`", "").replace("json", "")
            try:
                iters += 1
                rating = json.loads(raw_response)["IsComplete"]
                self.logger.log(f"Editor Determined IsComplete: {rating}", 5)
                return rating
            
            except Exception as e:
                if iters > 4:
                    self.logger.log("Critical Error Parsing JSON", 7)
                    return False
                self.logger.log("Error Parsing JSON Written By LLM, Asking For Edits", 7)
                edit_prompt = self.get_outline_prompt("json_parse_error").format(_Error=e)
                history.append(self.interface.build_user_query(edit_prompt))
                self.logger.log("Asking LLM TO Revise", 7)
                history = self.interface.generate_text(
                    self.logger, history, EVAL_MODEL, format="json"
                )
                self.logger.log("Done Asking LLM TO Revise JSON", 6)

    def revise_outline(self, outline: str, feedback: str, history: list = []):
        revision_prompt = self.get_outline_prompt("outline_revision").format(outline=outline, 
                                                        feedback=feedback)

        self.logger.log("Revising Outline", 2)
        messages = history
        messages.append(self.interface.build_user_query(revision_prompt))
        messages = self.interface.generate_text(
            self.logger, messages, INITIAL_OUTLINE_WRITER_MODEL, min_word_count=250
        )
        summary_text = self.interface.get_last_message_text(messages)
        self.logger.log("Done Revising Outline", 2)

        return summary_text, messages

    def generate_per_chapter_outline(
        self,
        chapter: int,
        outline: str,
        messages: List[Any]
    ) -> Tuple[str, List[Any]]:
        """Generate per-chapter outline."""

        chapter_outline_prompt = self.get_outline_prompt("chapter_outline").format(chapter=chapter, 
                                                                                   outline=outline)
        self.logger.log("Generating Outline For Chapter " + str(chapter), 5)
        messages_list = messages
        messages_list.append(self.interface.build_user_query(chapter_outline_prompt))
        messages_list = self.interface.generate_text(
            self.logger, messages_list, CHAPTER_OUTLINE_WRITER_MODEL, min_word_count=50
        )
        summary_text = self.interface.get_last_message_text(messages_list)
        self.logger.log("Done Generating Outline For Chapter " + str(chapter), 5)

        return summary_text, messages_list