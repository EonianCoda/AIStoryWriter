"""Outline generation utilities."""
import json
from typing import Any, Tuple, List
from writer.interface.wrapper import Interface
from writer.config import (
    INITIAL_OUTLINE_WRITER_MODEL,
    OUTLINE_MAX_REVISIONS,
    OUTLINE_MIN_REVISIONS,
    CHAPTER_OUTLINE_WRITER_MODEL,
)
from writer.prompts import (
    GET_IMPORTANT_BASE_PROMPT_INFO,
    STORY_ELEMENTS_PROMPT,
    INITIAL_OUTLINE_PROMPT,
    
    CRITIC_OUTLINE_INTRO,
    CRITIC_OUTLINE_PROMPT,
    
    OUTLINE_COMPLETE_INTRO,
    OUTLINE_COMPLETE_PROMPT,
    JSON_PARSE_ERROR,
    
    OUTLINE_REVISION_PROMPT,
    CHAPTER_OUTLINE_PROMPT,
)
# from writer.outline.story_elements import generate_story_elements
from writer.logger import Logger
from writer.config import REVISION_MODEL, EVAL_MODEL

class OutlineGenerator:
    def __init__(self, interface: Interface, logger: Logger):
        self.interface = interface
        self.logger = logger

    def generate_outline(self, user_story_prompt: str) -> Tuple[str, Any, Any, Any]:
        """Generate the story outline."""

        # 1. Extract Important Base Context
        prompt_info = GET_IMPORTANT_BASE_PROMPT_INFO.format(user_story_prompt=user_story_prompt)

        self.logger.log("Extracting Important Base Context", 4)
        messages = [self.interface.build_user_query(prompt_info)]
        messages = self.interface.generate_text(
            self.logger, messages, INITIAL_OUTLINE_WRITER_MODEL
        )
        base_context = self.interface.get_last_message_text(messages)
        self.logger.log("Done Extracting Important Base Context", 4)

        # 2. Generate Story Elements
        story_elements = self.generate_story_elements(user_story_prompt)
        
        # 3. Generate Initial Outline
        outline, writing_history = self.generate_initial_outline(user_story_prompt, story_elements)
        
        self.logger.log("Entering Feedback/Revision Loop", 3)
        rating: int| bool = 0
        iterations: int = 0
        
        while True:
            iterations += 1
            # 4. Get Feedback on Outline
            feedback = self.get_feedback_on_outline(outline)
            # 4.5 Get Rating on Outline
            rating = self.get_outline_rating(outline)
            # Currently get_outline_rating returns a bool - does it meet the standards (yes/no)?
            #TODO Future - could return a 0-100 int rating again if needed
                # Rating has been changed from a 0-100 int, to does it meet the standards (yes/no)?
                # Yes it has - the 0-100 int isn't actually good at all, LLM just returned a bunch of junk ratings

            # Check if retry iterations exceeded max, or if rating is good enough and min iterations met
            if (iterations > OUTLINE_MAX_REVISIONS) or (rating is True and iterations >= OUTLINE_MIN_REVISIONS):
                break
            
            # 5. Revise Outline (if rating not good enough)
            outline, writing_history = self.revise_outline(outline, feedback, writing_history)

        self.logger.log("Quality Standard Met, Exiting Feedback/Revision Loop", 4)

        final_outline: str = f"""{base_context}
        {story_elements}
        {outline}
"""  
        return final_outline, story_elements, outline, base_context

    def generate_story_elements(self, user_story_prompt: str):
        # Generate Initial Story Elements
        self.logger.log("Generating Main Story Elements", 4)

        story_elements_prompt = STORY_ELEMENTS_PROMPT.format(user_story_prompt=user_story_prompt)
        messages = [self.interface.build_user_query(story_elements_prompt)]
        messages = self.interface.generate_text(
            self.logger, messages, INITIAL_OUTLINE_WRITER_MODEL, min_word_count=150
        )
        elements = self.interface.get_last_message_text(messages)
        self.logger.log("Done Generating Main Story Elements", 4)

        return elements

    def generate_initial_outline(self, 
                         user_story_prompt: str,
                         story_elements: str):
        outline_prompt: str = INITIAL_OUTLINE_PROMPT.format(story_elements=story_elements, 
                                                            outline_prompt=user_story_prompt)

        self.logger.log("Generating Initial Outline", 4)
        messages = [self.interface.build_user_query(outline_prompt)]
        messages = self.interface.generate_text(
            self.logger, messages, INITIAL_OUTLINE_WRITER_MODEL, min_word_count=250
        )
        outline = self.interface.get_last_message_text(messages)
        self.logger.log("Done Generating Initial Outline", 4)
        
        return outline, messages

    def get_feedback_on_outline(self, outline: str) -> str:
        """Prompt LLM to critique outline."""
        history = []
        history.append(self.interface.build_system_query(CRITIC_OUTLINE_INTRO))
        critic_outline_prompt = CRITIC_OUTLINE_PROMPT.format(outline=outline)
        
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
        history.append(self.interface.build_system_query(OUTLINE_COMPLETE_INTRO)) # Character
        starting_prompt = OUTLINE_COMPLETE_PROMPT.format(outline=outline)
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
                edit_prompt = JSON_PARSE_ERROR.format(_Error=e)
                history.append(self.interface.build_user_query(edit_prompt))
                self.logger.log("Asking LLM TO Revise", 7)
                history = self.interface.generate_text(
                    self.logger, history, EVAL_MODEL, format="json"
                )
                self.logger.log("Done Asking LLM TO Revise JSON", 6)

    def revise_outline(self, outline: str, feedback: str, history: list = []):
        revision_prompt = OUTLINE_REVISION_PROMPT.format(outline=outline, 
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
    interface: Interface,
    logger: Any,
    chapter: int,
    outline: str,
    messages: List[Any]
) -> Tuple[str, List[Any]]:
    """Generate per-chapter outline."""

    revision_prompt: str = CHAPTER_OUTLINE_PROMPT.format(
        _Chapter=chapter,
        _Outline=outline
    )
    logger.log("Generating Outline For Chapter " + str(chapter), 5)
    messages_list = messages
    messages_list.append(interface.build_user_query(revision_prompt))
    messages_list = interface.generate_text(
        logger, messages_list, CHAPTER_OUTLINE_WRITER_MODEL, min_word_count=50
    )
    summary_text: str = interface.get_last_message_text(messages_list)
    logger.log("Done Generating Outline For Chapter " + str(chapter), 5)

    return summary_text, messages_list