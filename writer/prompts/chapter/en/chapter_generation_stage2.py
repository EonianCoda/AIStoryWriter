CHAPTER_GENERATION_STAGE2 = '''
{ContextHistoryInsert}

{_BaseContext}

Please write character development for the following chapter {_ChapterNum} of {_TotalChapters} based on the following criteria and any previous chapters.
Pay attention to the previous chapters, and make sure you both continue seamlessly from them, It's imperative that your writing connects well with the previous chapter, and flows into the next (so try to follow the outline)!

Don't take away content, instead expand upon it to make a longer and more detailed output.

For your reference, here is my outline for this chapter:
<CHAPTER_OUTLINE>
{ThisChapterOutline}
</CHAPTER_OUTLINE>

{FormattedLastChapterSummary}

And here is what I have for the current chapter's plot:
<CHAPTER_PLOT>
{Stage1Chapter}
</CHAPTER_PLOT>

As a reminder to keep the following criteria in mind as you expand upon the above work:
    - Characters: Who are the characters in this chapter? What do they mean to each other? What is the situation between them? Is it a conflict? Is there tension? Is there a reason that the characters have been brought together?
    - Development: What are the goals of each character, and do they meet those goals? Do the characters change and exhibit growth? Do the goals of each character change over the story?
    - Details: How are things described? Is it repetitive? Is the word choice appropriate for the scene? Are we describing things too much or too little?

Don't answer these questions directly, instead make your writing implicitly answer them. (Show, don't tell)

Make sure that your chapter flows into the next and from the previous (if applicable).

Remember, have fun, be creative, and improve the character development of chapter {_ChapterNum} (make sure you only write this one)!

{Feedback}'''