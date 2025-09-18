"""Utility functions for printing and logging."""
import termcolor
import datetime
import os
import json
from typing import Any


def print_message_history(messages):
    print("------------------------------------------------------------")
    for message in messages:
        print(message)
    print("------------------------------------------------------------")


class Logger:
    """Logger for system messages."""

    def __init__(self, logfile_prefix="Logs") -> None:
        # Make Paths For Log
        log_dir_path = logfile_prefix + "/Generation_" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        os.makedirs(log_dir_path + "/LangchainDebug", exist_ok=True)

        # Setup Log Path
        self.log_dir_prefix = log_dir_path
        self.log_path = log_dir_path + "/Main.log"
        self.file = open(self.log_path, "a")
        self.langchain_id = 0

        self.log_items = []


    # Helper function that saves the entire language chain object as both json and markdown for debugging later
    def save_lang_chain(self, lang_chain_id: str, lang_chain: list):

        # Calculate Filepath For This Langchain
        log_path_json: str = self.log_dir_prefix + f"/LangchainDebug/{self.langchain_id}_{lang_chain_id}.json"
        log_path_md: str = self.log_dir_prefix + f"/LangchainDebug/{self.langchain_id}_{lang_chain_id}.md"
        lang_chain_debug_title: str = f"{self.langchain_id}_{lang_chain_id}"
        self.langchain_id += 1

        # Generate and Save JSON Version
        with open(log_path_json, "w", encoding="utf-8") as f:
            f.write(json.dumps(lang_chain, indent=4, sort_keys=True))
        
        # Now, Save Markdown Version
        with open(log_path_md, "w", encoding="utf-8") as f:
            markdown_version: str = f"# Debug LangChain {lang_chain_debug_title}\n**Note: '```' tags have been removed in this version.**\n"
            for message in lang_chain:
                markdown_version += f"\n\n\n# Role: {message['role']}\n"
                markdown_version += f"```{message['content'].replace('```', '')}```"
            f.write(markdown_version)
        
        self.log(f"Wrote This Language Chain ({lang_chain_debug_title}) To Debug File {log_path_md}", 5)


    # Saves the given story to disk
    def save_story(self, story_content: str) -> None:

        with open(f"{self.log_dir_prefix}/Story.md", "w", encoding="utf-8") as f:
            f.write(story_content)

        self.log(f"Wrote Story To Disk At {self.log_dir_prefix}/Story.md", 5)


    # Logs an item
    def log(self, item, level: int) -> None:

        # Create Log Entry
        log_entry = f"[{str(level).ljust(2)}] [{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}] {item}"

        # Write it to file
        self.file.write(log_entry + "\n")
        self.log_items.append(log_entry)

        # Now color and print it
        if (level == 0):
            log_entry = termcolor.colored(log_entry, "white")
        elif (level == 1):
            log_entry = termcolor.colored(log_entry, "grey")
        elif (level == 2):
            log_entry = termcolor.colored(log_entry, "blue")
        elif (level == 3):
            log_entry = termcolor.colored(log_entry, "cyan")
        elif (level == 4):
            log_entry = termcolor.colored(log_entry, "magenta")
        elif (level == 5):
            log_entry = termcolor.colored(log_entry, "green")
        elif (level == 6):
            log_entry = termcolor.colored(log_entry, "yellow")
        elif (level == 7):
            log_entry = termcolor.colored(log_entry, "red")

        print(log_entry)


    def __del__(self):
        self.file.close()