CHAPTER_TO_SCENES = """
# CONTEXT #
I am writing a story and need your help with dividing chapters into scenes. Below is my outline so far:
```
{_Outline}
```
###############

# OBJECTIVE #
Create a scene-by-scene outline for the chapter that helps me write better scenes.
Make sure to include information about each scene that describes what happens, in what tone it's written, who the characters in the scene are, and what the setting is.
Here's the specific chapter outline that we need to split up into scenes:
```
{_ThisChapter}
```
###############

# STYLE #
Provide a creative response that helps add depth and plot to the story, but still follows the outline.
Make your response markdown-formatted so that the details and information about the scene are clear.

Above all, make sure to be creative and original when writing.
###############

# AUDIENCE #
Please tailor your response to another creative writer.
###############

# RESPONSE #
Be detailed and well-formatted in your response, yet ensure you have a well-thought out and creative output.
###############
"""

SCENES_TO_JSON = """
# CONTEXT #
I need to convert the following scene-by-scene outline into a JSON formatted list.
```
{_Scenes}
```
###############

# OBJECTIVE #
Create a JSON list of each of scene from the provided outline where each element in the list contains the content for that scene.
Ex:
[
    "scene 1 content...",
    "scene 2 content...",
    "etc."
]

Don't include any other json fields, just make it a simple list of strings.
###############

# STYLE #
Respond in pure JSON.
###############

# AUDIENCE #
Please tailor your response such that it is purely JSON formatted.
###############

# RESPONSE #
Don't lose any information from the original outline, just format it to fit in a list.
###############
"""

SCENE_OUTLINE_TO_SCENE = """
# CONTEXT #
I need your assistance writing the full scene based on the following scene outline.
```
{_SceneOutline}
```

For context, here is the full outline of the story.
```
{_Outline}
```
###############

# OBJECTIVE #
Create a full scene based on the given scene outline, that is written in the appropriate tone for the scene.
Make sure to include dialogue and other writing elements as needed.
###############

# STYLE #
Make your style be creative and appropriate for the given scene. The scene outline should indicate the right style, but if not use your own judgement.
###############

# AUDIENCE #
Please tailor your response to be written for the general public's entertainment as a creative writing piece.
###############

# RESPONSE #
Make sure your response is well thought out and creative. Take a moment to make sure it follows the provided scene outline, and ensure that it also fits into the main story outline.
###############
"""