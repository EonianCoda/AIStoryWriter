import writer.llm_editor
import writer.print_utils
import writer.config
import writer.chapter.chapter_gen_summary_check
import writer.prompts
import writer.scene.chapter_outline_to_scenes
import writer.scene.scenes_to_json
import writer.scene.scene_outline_to_scene
from writer.interface.wrapper import Interface

def chapter_by_scene(interface: Interface, logger, this_chapter: str, outline: str, base_context: str = ""):
    # This function calls all other scene-by-scene generation functions and creates a full chapter based on the new scene pipeline.

    logger.log(f"Starting Scene-By-Scene Chapter Generation Pipeline", 2)

    scene_by_scene_outline = writer.scene.chapter_outline_to_scenes.chapter_outline_to_scenes(
        interface, logger, this_chapter, outline, _BaseContext=base_context
    )

    scene_json_list = writer.scene.scenes_to_json.scenes_to_json(interface, logger, scene_by_scene_outline)

    # Now we iterate through each scene one at a time and write it, then add it to this rough chapter, which is then returned for further editing
    rough_chapter: str = ""
    for scene in scene_json_list:
        rough_chapter += writer.scene.scene_outline_to_scene.scene_outline_to_scene(
            interface, logger, scene, outline, base_context
        )

    logger.log(f"Starting Scene-By-Scene Chapter Generation Pipeline", 2)

    return rough_chapter
