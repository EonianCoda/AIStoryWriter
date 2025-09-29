CHAPTER_GENERATION_STAGE1 = '''
{ContextHistoryInsert}

{_BaseContext}

Please write the plot for chapter {_ChapterNum} of {_TotalChapters} based on the following chapter outline and any previous chapters.
Pay attention to the previous chapters, and make sure you both continue seamlessly from them, It's imperative that your writing connects well with the previous chapter, and flows into the next (so try to follow the outline)!

Here is my outline for this chapter:
<CHAPTER_OUTLINE>
{ThisChapterOutline}
</CHAPTER_OUTLINE>

{FormattedLastChapterSummary}

As you write your work, please use the following suggestions to help you write chapter {_ChapterNum} (make sure you only write this one):
    - Pacing: 
    - Are you skipping days at a time? Summarizing events? Don't do that, add scenes to detail them.
    - Is the story rushing over certain plot points and excessively focusing on others?
    - Flow: Does each chapter flow into the next? Does the plot make logical sense to the reader? Does it have a specific narrative structure at play? Is the narrative structure consistent throughout the story?
    - Genre: What is the genre? What language is appropriate for that genre? Do the scenes support the genre?

{Feedback}'''