SUMMARY_CHECK_INTRO = "You are a helpful AI Assistant. Answer the user's prompts to the best of your abilities."

SUMMARY_CHECK_PROMPT = """
Please summarize the following chapter:

<CHAPTER>
{_Work}
</CHAPTER>

Do not include anything in your response except the summary."""

SUMMARY_OUTLINE_INTRO = "You are a helpful AI Assistant. Answer the user's prompts to the best of your abilities."

SUMMARY_OUTLINE_PROMPT = """
Please summarize the following chapter outline:

<OUTLINE>
{_RefSummary}
</OUTLINE>

Do not include anything in your response except the summary."""

SUMMARY_COMPARE_INTRO = "You are a helpful AI Assistant. Answer the user's prompts to the best of your abilities."

SUMMARY_COMPARE_PROMPT = """
Please compare the provided summary of a chapter and the associated outline, and indicate if the provided content roughly follows the outline.

Please write a JSON formatted response with no other content with the following keys.
Note that a computer is parsing this JSON so it must be correct.

<CHAPTER_SUMMARY>
{WorkSummary}
</CHAPTER_SUMMARY>

<OUTLINE>
{OutlineSummary}
</OUTLINE>

Please respond with the following JSON fields:

{{
"Suggestions": str
"DidFollowOutline": true/false
}}

Suggestions should include a string containing detailed markdown formatted feedback that will be used to prompt the writer on the next iteration of generation.
Specify general things that would help the writer remember what to do in the next iteration.
It will not see the current chapter, so feedback specific to this one is not helpful, instead specify areas where it needs to pay attention to either the prompt or outline.
The writer is also not aware of each iteration - so provide detailed information in the prompt that will help guide it.
Start your suggestions with 'Important things to keep in mind as you write: \n'.

It's okay if the summary isn't a complete perfect match, but it should have roughly the same plot, and pacing.

Again, remember to make your response JSON formatted with no extra words. It will be fed directly to a JSON parser.
"""