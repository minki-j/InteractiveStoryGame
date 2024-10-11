from fasthtml.common import *
from app.views.components.error_responses import error_modal
from app.agents.main_graph import main_graph
from db import db, Stories, Scene  # Import Stories and Scene

from app.agents.state_schema import Scene


async def generate_scene(req, id: str):
    print("\n>>> CNTRL generate_scene")

    story_data = db.t.stories.get(id)

    if not story_data:
        raise Exception(f"Story data not found for story_id: {id}")

    config = {"configurable": {"thread_id": id}}

    state = main_graph.get_state(config)
    if not state.values["is_prologue_completed"]:
        main_graph.update_state(
            config,
            {"is_prologue_completed": True},
        )

    r = main_graph.invoke(None, config)

    if r:
        story_data.scenes = [Scene(**scene_data) for scene_data in r["story"]]

        db.t.stories.update(
            pk_values=id,
            updates={
                "scenes": story_data.scenes
            },  # use custom setter that serializes Scene objects
        )

        return RedirectResponse(url=f"/story?id={id}", status_code=303)
    else:
        return error_modal("An error happened at generate_scene")
