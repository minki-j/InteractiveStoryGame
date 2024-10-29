import json

from fasthtml.common import *
from app.views.components.error_responses import error_modal
from app.agents.main_graph import main_graph
from db import db

async def generate_scene(session, req: Request, id: str):
    print("\n>>> CNTRL generate_scene")

    story_data = db.t.stories.get(id)

    if not story_data:
        raise Exception(f"Story data not found for story_id: {id}")

    config = {"configurable": {"thread_id": id}}

    state = main_graph.get_state(config, subgraphs=True)

    if not state.values["is_prologue_completed"]:
        main_graph.update_state(
            config,
            {"is_prologue_completed": True},
        )
    else:
        print(req)
        form_data = await req.form()
        print(f"==>> form_data: {form_data}")
        user_choice = form_data.get("chosen_option_index", "-1")
        subgraph_config = state.tasks[0].state.config
        main_graph.update_state(
            subgraph_config,
            {
                "user_choice": int(user_choice),
                "custom_user_choice": form_data.get("custom_user_choice", None),
            },
        )

    r = main_graph.invoke(None, config)

    if r:
        state = main_graph.get_state(config, subgraphs=True)
        subgraph_state = state.tasks[0].state.values

        db.t.stories.update(
            pk_values=id,
            updates={
                "scenes": json.dumps(
                    [scene.model_dump() for scene in subgraph_state["story"]]
                )
            },
        )

        return RedirectResponse(url=f"/story?id={id}", status_code=303)
    else:
        return error_modal("An error happened at main_graph while generating a scene")
