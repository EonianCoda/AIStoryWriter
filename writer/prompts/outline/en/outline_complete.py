OUTLINE_COMPLETE = '''
<OUTLINE>
{outline}
</OUTLINE>

This outline meets all of the following criteria (true or false):
  - Pacing: Is the story rushing over certain plot points and excessively focusing on others?
  - Details: How are things described? Is it repetitive? Is the word choice appropriate for the scene? Are we describing things too much or too little?
  - Flow: Does each chapter flow into the next? Does the plot make logical sense to the reader? Does it have a specific narrative structure at play? Is the narrative structure consistent throughout the story?
  - Genre: What is the genre? What language is appropriate for that genre? Do the scenes support the genre?

Give a JSON formatted response, containing the string "IsComplete", followed by an boolean True/False.
Please do not include any other text, just the JSON as your response will be parsed by a computer.
'''