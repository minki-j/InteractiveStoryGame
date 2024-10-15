import json
from fasthtml.common import *

from db import db
from app.agents.main_graph import main_graph


async def apply_feedback_to_prologue(session, req: Request, id: str):
    print("\n>>> CONTROLLER apply_feedback_to_prologue")

    config = {"configurable": {"thread_id": id}, "recursion_limit": 100}

    form_data = await req.form()
    main_graph.update_state(
        config,
        {"prologue_feedback": form_data.get("feedback")},
    )

    response = main_graph.invoke(None, config)

    if response:
        db.t.stories.update(
            pk_values=id,
            updates={
                "title": response["title"],
                "prologue": response["prologue"],
            },
        )

    return RedirectResponse(url=f"/prologue?id={id}", status_code=303)
