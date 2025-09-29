EXTRA_PROMPT_INFO_GENERATION = '''
Please extract any important information from the user's prompt below:

<USER_PROMPT>
{user_story_prompt}
</USER_PROMPT>

Just write down any information that wouldn't be covered in an outline.
Please use the below template for formatting your response.
This would be things like instructions for chapter length, overall vision, instructions for formatting, etc.
(Don't use the xml tags though - those are for example only)

<EXAMPLE>
# Important Additional Context
- Important point 1
- Important point 2
</EXAMPLE>

Do NOT write the outline itself, just some extra context. Keep your responses short.
'''