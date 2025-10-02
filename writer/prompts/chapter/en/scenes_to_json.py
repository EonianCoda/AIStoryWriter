SCENES_TO_JSON = '''# CONTEXT
I need to convert the following scene-by-scene outline into a JSON formatted list.
```
{scenes}
```
# OBJECTIVE
Create a JSON list of each of scene from the provided outline where each element in the list contains the content for that scene.
Ex:
[
    "scene 1 content...",
    "scene 2 content...",
    "etc."
]

Don't include any other json fields, just make it a simple list of strings.

# STYLE
Respond in pure JSON.

# AUDIENCE
Please tailor your response such that it is purely JSON formatted.

# RESPONSE
Don't lose any information from the original outline, just format it to fit in a list.
'''