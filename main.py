#!/bin/python3

import argparse
import time
import datetime
import os
import json

import writer.config

import writer.interface.wrapper
import writer.print_utils
import writer.chapter.chapter_detector
import writer.scrubber
import writer.statistics
import writer.outline_generator
import writer.chapter.chapter_generator
import writer.story_info
import writer.novel_editor
import writer.translator


# Setup Argparser
Parser = argparse.ArgumentParser()
Parser.add_argument("-Prompt", help="Path to file containing the prompt")
Parser.add_argument(
    "-Output",
    default="",
    type=str,
    help="Optional file output path, if none is speciifed, we will autogenerate a file name based on the story title",
)
Parser.add_argument(
    "-InitialOutlineModel",
    default=writer.config.INITIAL_OUTLINE_WRITER_MODEL,
    type=str,
    help="Model to use for writing the base outline content",
)
Parser.add_argument(
    "-ChapterOutlineModel",
    default=writer.config.CHAPTER_OUTLINE_WRITER_MODEL,
    type=str,
    help="Model to use for writing the per-chapter outline content",
)
Parser.add_argument(
    "-ChapterS1Model",
    default=writer.config.CHAPTER_STAGE1_WRITER_MODEL,
    type=str,
    help="Model to use for writing the chapter (stage 1: plot)",
)
Parser.add_argument(
    "-ChapterS2Model",
    default=writer.config.CHAPTER_STAGE2_WRITER_MODEL,
    type=str,
    help="Model to use for writing the chapter (stage 2: character development)",
)
Parser.add_argument(
    "-ChapterS3Model",
    default=writer.config.CHAPTER_STAGE3_WRITER_MODEL,
    type=str,
    help="Model to use for writing the chapter (stage 3: dialogue)",
)
Parser.add_argument(
    "-ChapterS4Model",
    default=writer.config.CHAPTER_STAGE4_WRITER_MODEL,
    type=str,
    help="Model to use for writing the chapter (stage 4: final correction pass)",
)
Parser.add_argument(
    "-ChapterRevisionModel",
    default=writer.config.CHAPTER_REVISION_WRITER_MODEL,
    type=str,
    help="Model to use for revising the chapter until it meets criteria",
)
Parser.add_argument(
    "-RevisionModel",
    default=writer.config.REVISION_MODEL,
    type=str,
    help="Model to use for generating constructive criticism",
)
Parser.add_argument(
    "-EvalModel",
    default=writer.config.EVAL_MODEL,
    type=str,
    help="Model to use for evaluating the rating out of 100",
)
Parser.add_argument(
    "-InfoModel",
    default=writer.config.INFO_MODEL,
    type=str,
    help="Model to use when generating summary/info at the end",
)
Parser.add_argument(
    "-ScrubModel",
    default=writer.config.SCRUB_MODEL,
    type=str,
    help="Model to use when scrubbing the story at the end",
)
Parser.add_argument(
    "-CheckerModel",
    default=writer.config.CHECKER_MODEL,
    type=str,
    help="Model to use when checking if the LLM cheated or not",
)
Parser.add_argument(
    "-TranslatorModel",
    default=writer.config.TRANSLATOR_MODEL,
    type=str,
    help="Model to use if translation of the story is enabled",
)
Parser.add_argument(
    "-Translate",
    default="",
    type=str,
    help="Specify a language to translate the story to - will not translate by default. Ex: 'French'",
)
Parser.add_argument(
    "-TranslatePrompt",
    default="",
    type=str,
    help="Specify a language to translate your input prompt to. Ex: 'French'",
)
Parser.add_argument("-Seed", default=12, type=int, help="Used to seed models.")
Parser.add_argument(
    "-OutlineMinRevisions",
    default=0,
    type=int,
    help="Number of minimum revisions that the outline must be given prior to proceeding",
)
Parser.add_argument(
    "-OutlineMaxRevisions",
    default=3,
    type=int,
    help="Max number of revisions that the outline may have",
)
Parser.add_argument(
    "-ChapterMinRevisions",
    default=0,
    type=int,
    help="Number of minimum revisions that the chapter must be given prior to proceeding",
)
Parser.add_argument(
    "-ChapterMaxRevisions",
    default=3,
    type=int,
    help="Max number of revisions that the chapter may have",
)
Parser.add_argument(
    "-NoChapterRevision", action="store_true", help="Disables Chapter Revisions"
)
Parser.add_argument(
    "-NoScrubChapters",
    action="store_true",
    help="Disables a final pass over the story to remove prompt leftovers/outline tidbits",
)
Parser.add_argument(
    "-ExpandOutline",
    action="store_true",
    default=True,
    help="Disables the system from expanding the outline for the story chapter by chapter prior to writing the story's chapter content",
)
Parser.add_argument(
    "-EnableFinalEditPass",
    action="store_true",
    help="Enable a final edit pass of the whole story prior to scrubbing",
)
Parser.add_argument(
    "-Debug",
    action="store_true",
    help="Print system prompts to stdout during generation",
)
Parser.add_argument(
    "-SceneGenerationPipeline",
    action="store_true",
    default=True,
    help="Use the new scene-by-scene generation pipeline as an initial starting point for chapter writing",
)
Args = Parser.parse_args()


# Measure Generation Time
StartTime = time.time()


# Setup config
writer.config.SEED = Args.Seed

writer.config.INITIAL_OUTLINE_WRITER_MODEL = Args.InitialOutlineModel
writer.config.CHAPTER_OUTLINE_WRITER_MODEL = Args.ChapterOutlineModel
writer.config.CHAPTER_STAGE1_WRITER_MODEL = Args.ChapterS1Model
writer.config.CHAPTER_STAGE2_WRITER_MODEL = Args.ChapterS2Model
writer.config.CHAPTER_STAGE3_WRITER_MODEL = Args.ChapterS3Model
writer.config.CHAPTER_STAGE4_WRITER_MODEL = Args.ChapterS4Model
writer.config.CHAPTER_REVISION_WRITER_MODEL = Args.ChapterRevisionModel
writer.config.EVAL_MODEL = Args.EvalModel
writer.config.REVISION_MODEL = Args.RevisionModel
writer.config.INFO_MODEL = Args.InfoModel
writer.config.SCRUB_MODEL = Args.ScrubModel
writer.config.CHECKER_MODEL = Args.CheckerModel
writer.config.TRANSLATOR_MODEL = Args.TranslatorModel

writer.config.TRANSLATE_LANGUAGE = Args.Translate
writer.config.TRANSLATE_PROMPT_LANGUAGE = Args.TranslatePrompt

writer.config.OUTLINE_MIN_REVISIONS = Args.OutlineMinRevisions
writer.config.OUTLINE_MAX_REVISIONS = Args.OutlineMaxRevisions

writer.config.CHAPTER_MIN_REVISIONS = Args.ChapterMinRevisions
writer.config.CHAPTER_MAX_REVISIONS = Args.ChapterMaxRevisions
writer.config.CHAPTER_NO_REVISIONS = Args.NoChapterRevision

writer.config.SCRUB_NO_SCRUB = Args.NoScrubChapters
writer.config.EXPAND_OUTLINE = Args.ExpandOutline
writer.config.ENABLE_FINAL_EDIT_PASS = Args.EnableFinalEditPass

writer.config.OPTIONAL_OUTPUT_NAME = Args.Output
writer.config.SCENE_GENERATION_PIPELINE = Args.SceneGenerationPipeline
writer.config.DEBUG = Args.Debug

# Get a list of all used providers
Models = [
    writer.config.INITIAL_OUTLINE_WRITER_MODEL,
    writer.config.CHAPTER_OUTLINE_WRITER_MODEL,
    writer.config.CHAPTER_STAGE1_WRITER_MODEL,
    writer.config.CHAPTER_STAGE2_WRITER_MODEL,
    writer.config.CHAPTER_STAGE3_WRITER_MODEL,
    writer.config.CHAPTER_STAGE4_WRITER_MODEL,
    writer.config.CHAPTER_REVISION_WRITER_MODEL,
    writer.config.EVAL_MODEL,
    writer.config.REVISION_MODEL,
    writer.config.INFO_MODEL,
    writer.config.SCRUB_MODEL,
    writer.config.CHECKER_MODEL,
    writer.config.TRANSLATOR_MODEL,
]
Models = list(set(Models))

# Setup Logger
SysLogger = writer.print_utils.Logger()

# Initialize interface
SysLogger.Log("Created OLLAMA interface", 5)
interface = writer.interface.wrapper.Interface(Models)

# Load User Prompt
Prompt: str = ""
if Args.Prompt is None:
    raise Exception("No Prompt Provided")
with open(Args.Prompt, "r", encoding="utf-8") as f:
    Prompt = f.read()


# If user wants their prompt translated, do so
if writer.config.TRANSLATE_PROMPT_LANGUAGE != "":
    Prompt = writer.translator.TranslatePrompt(
        interface, SysLogger, Prompt, writer.config.TRANSLATE_PROMPT_LANGUAGE
    )


# Generate the Outline
Outline, Elements, RoughChapterOutline, BaseContext = writer.outline_generator.GenerateOutline(
    interface, SysLogger, Prompt, writer.config.OUTLINE_QUALITY
)
BasePrompt = Prompt


# Detect the number of chapters
SysLogger.Log("Detecting Chapters", 5)
Messages = [interface.BuildUserQuery(Outline)]
NumChapters: int = writer.chapter.chapter_detector.LLMCountChapters(
    interface, SysLogger, interface.GetLastMessageText(Messages)
)
SysLogger.Log(f"Found {NumChapters} Chapter(s)", 5)


## Write Per-Chapter Outline
Prompt = f"""
Please help me expand upon the following outline, chapter by chapter.

```
{Outline}
```
    
"""
Messages = [interface.BuildUserQuery(Prompt)]
ChapterOutlines: list = []
if writer.config.EXPAND_OUTLINE:
    for Chapter in range(1, NumChapters + 1):
        ChapterOutline, Messages = writer.outline_generator.GeneratePerChapterOutline(
            interface, SysLogger, Chapter, Outline, Messages
        )
        ChapterOutlines.append(ChapterOutline)


# Create MegaOutline
DetailedOutline: str = ""
for Chapter in ChapterOutlines:
    DetailedOutline += Chapter
MegaOutline: str = f"""

# Base Outline
{Elements}

# Detailed Outline
{DetailedOutline}

"""

# Setup Base Prompt For Per-Chapter Generation
UsedOutline: str = Outline
if writer.config.EXPAND_OUTLINE:
    UsedOutline = MegaOutline


# Write the chapters
SysLogger.Log("Starting Chapter Writing", 5)
Chapters = []
for i in range(1, NumChapters + 1):

    Chapter = writer.chapter.chapter_generator.GenerateChapter(
        interface,
        SysLogger,
        i,
        NumChapters,
        Outline,
        Chapters,
        writer.config.OUTLINE_QUALITY,
        BaseContext,
    )

    Chapter = f"### Chapter {i}\n\n{Chapter}"
    Chapters.append(Chapter)
    ChapterWordCount = writer.statistics.GetWordCount(Chapter)
    SysLogger.Log(f"Chapter Word Count: {ChapterWordCount}", 2)


# Now edit the whole thing together
StoryBodyText: str = ""
StoryInfoJSON:dict = {"Outline": Outline}
StoryInfoJSON.update({"StoryElements": Elements})
StoryInfoJSON.update({"RoughChapterOutline": RoughChapterOutline})
StoryInfoJSON.update({"BaseContext": BaseContext})

if writer.config.ENABLE_FINAL_EDIT_PASS:
    NewChapters = writer.novel_editor.EditNovel(
        interface, SysLogger, Chapters, Outline, NumChapters
    )
NewChapters = Chapters
StoryInfoJSON.update({"UnscrubbedChapters": NewChapters})

# Now scrub it (if enabled)
if not writer.config.SCRUB_NO_SCRUB:
    NewChapters = writer.scrubber.ScrubNovel(
        interface, SysLogger, NewChapters, NumChapters
    )
else:
    SysLogger.Log(f"Skipping Scrubbing Due To config", 4)
StoryInfoJSON.update({"ScrubbedChapter": NewChapters})


# If enabled, translate the novel
if writer.config.TRANSLATE_LANGUAGE != "":
    NewChapters = writer.translator.TranslateNovel(
        interface, SysLogger, NewChapters, NumChapters, writer.config.TRANSLATE_LANGUAGE
    )
else:
    SysLogger.Log(f"No Novel Translation Requested, Skipping Translation Step", 4)
StoryInfoJSON.update({"TranslatedChapters": NewChapters})


# Compile The Story
for Chapter in NewChapters:
    StoryBodyText += Chapter + "\n\n\n"


# Now Generate Info
Messages = []
Messages.append(interface.BuildUserQuery(Outline))
Info = writer.story_info.GetStoryInfo(interface, SysLogger, Messages)
Title = Info["Title"]
StoryInfoJSON.update({"Title": Info["Title"]})
Summary = Info["Summary"]
StoryInfoJSON.update({"Summary": Info["Summary"]})
Tags = Info["Tags"]
StoryInfoJSON.update({"Tags": Info["Tags"]})

print("---------------------------------------------")
print(f"Story Title: {Title}")
print(f"Summary: {Summary}")
print(f"Tags: {Tags}")
print("---------------------------------------------")

ElapsedTime = time.time() - StartTime


# Calculate Total Words
TotalWords: int = writer.statistics.GetWordCount(StoryBodyText)
SysLogger.Log(f"Story Total Word Count: {TotalWords}", 4)

StatsString: str = "Work Statistics:  \n"
StatsString += " - Total Words: " + str(TotalWords) + "  \n"
StatsString += f" - Title: {Title}  \n"
StatsString += f" - Summary: {Summary}  \n"
StatsString += f" - Tags: {Tags}  \n"
StatsString += f" - Generation Start Date: {datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}  \n"
StatsString += f" - Generation Total Time: {ElapsedTime}s  \n"
StatsString += f" - Generation Average WPM: {60 * (TotalWords/ElapsedTime)}  \n"

StatsString += "\n\nUser Settings:  \n"
StatsString += f" - Base Prompt: {BasePrompt}  \n"

StatsString += "\n\nGeneration Settings:  \n"
StatsString += f" - Generator: AIStoryGenerator_2024-06-27  \n"
StatsString += (
    f" - Base Outline writer Model: {writer.config.INITIAL_OUTLINE_WRITER_MODEL}  \n"
)
StatsString += (
    f" - Chapter Outline writer Model: {writer.config.CHAPTER_OUTLINE_WRITER_MODEL}  \n"
)
StatsString += f" - Chapter writer (Stage 1: Plot) Model: {writer.config.CHAPTER_STAGE1_WRITER_MODEL}  \n"
StatsString += f" - Chapter writer (Stage 2: Char Development) Model: {writer.config.CHAPTER_STAGE2_WRITER_MODEL}  \n"
StatsString += f" - Chapter writer (Stage 3: Dialogue) Model: {writer.config.CHAPTER_STAGE3_WRITER_MODEL}  \n"
StatsString += f" - Chapter writer (Stage 4: Final Pass) Model: {writer.config.CHAPTER_STAGE4_WRITER_MODEL}  \n"
StatsString += f" - Chapter writer (Revision) Model: {writer.config.CHAPTER_REVISION_WRITER_MODEL}  \n"
StatsString += f" - Revision Model: {writer.config.REVISION_MODEL}  \n"
StatsString += f" - Eval Model: {writer.config.EVAL_MODEL}  \n"
StatsString += f" - Info Model: {writer.config.INFO_MODEL}  \n"
StatsString += f" - Scrub Model: {writer.config.SCRUB_MODEL}  \n"
StatsString += f" - Seed: {writer.config.SEED}  \n"
# StatsString += f" - Outline Quality: {writer.config.OUTLINE_QUALITY}  \n"
StatsString += f" - Outline Min Revisions: {writer.config.OUTLINE_MIN_REVISIONS}  \n"
StatsString += f" - Outline Max Revisions: {writer.config.OUTLINE_MAX_REVISIONS}  \n"
# StatsString += f" - Chapter Quality: {writer.config.CHAPTER_QUALITY}  \n"
StatsString += f" - Chapter Min Revisions: {writer.config.CHAPTER_MIN_REVISIONS}  \n"
StatsString += f" - Chapter Max Revisions: {writer.config.CHAPTER_MAX_REVISIONS}  \n"
StatsString += f" - Chapter Disable Revisions: {writer.config.CHAPTER_NO_REVISIONS}  \n"
StatsString += f" - Disable Scrubbing: {writer.config.SCRUB_NO_SCRUB}  \n"


# Save The Story To Disk
SysLogger.Log("Saving Story To Disk", 3)
os.makedirs("Stories", exist_ok=True)
FName = f"Stories/Story_{Title.replace(' ', '_')}"
if writer.config.OPTIONAL_OUTPUT_NAME != "":
    FName = writer.config.OPTIONAL_OUTPUT_NAME
with open(f"{FName}.md", "w", encoding="utf-8") as F:
    Out = f"""
{StatsString}

---

Note: An outline of the story is available at the bottom of this document.
Please scroll to the bottom if you wish to read that.

---
# {Title}

{StoryBodyText}


---
# Outline
```
{Outline}
```
"""
    SysLogger.SaveStory(Out)
    F.write(Out)

# Save JSON
with open(f"{FName}.json", "w", encoding="utf-8") as F:
    F.write(json.dumps(StoryInfoJSON, indent=4))