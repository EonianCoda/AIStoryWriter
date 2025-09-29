from typing import Any, Tuple, List
from writer.interface.wrapper import Interface
from writer.prompts import load_prompt
from writer.logger import Logger

class Generator:
    def __init__(self, interface: Interface, logger: Logger, language: str = "zh-tw") -> None:
        self.interface = interface
        self.logger = logger
        self.language = language
        
    def get_outline_prompt(self, prompt_name: str) -> str:
        """Load the appropriate prompt based on language and prompt name."""
        return load_prompt("outline", self.language, prompt_name)

    def get_chapter_prompt(self, prompt_name: str) -> str:
        return load_prompt("chapter", self.language, prompt_name)

    def get_character_prompt(self, character: str) -> str:
        return load_prompt("system_character", self.language, character)
    
    @property
    def novelist(self):
        return self.get_character_prompt("novelist2")
    
    @property
    def critic(self):
        return self.get_character_prompt("critic")
