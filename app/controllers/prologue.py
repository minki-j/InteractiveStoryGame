from fasthtml.common import *

from db import db
from app.agents.main_graph import main_graph


async def apply_feedback_to_prologue(req: Request, id: str):
    print("\n>>> CONTROLLER apply_feedback_to_prologue")
    form_data = await req.form()

    response = main_graph.invoke(
        input={
            "prologue_feedback": form_data.get("feedback"),
        },
        config={"configurable": {"thread_id": id}, "recursion_limit": 100},
    )

    print(f"==>> Response: {response}")

    if response:
        db.t.stories.update(pk_values=id, updates={"prologue": response["prologue"]})

    return RedirectResponse(url=f"/prologue?id={id}", status_code=303)
