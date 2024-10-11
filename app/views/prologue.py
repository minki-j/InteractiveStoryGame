from fasthtml.common import *

from db import db
from app.agents.main_graph import main_graph


def prologue_view(req: Request, id: str):
    print("\n>>> VIEW story_view")

    story_data = db.t.stories.get(id)

    if not story_data:
        raise Exception(f"Story data not found for story_id: {id}")

    return (
        Title("Story"),
        Main(cls="container")(
            A(href="/", style="text-decoration: none; color: inherit;")(
                H1("Story Sim")
            ),
            P(cls="marked")(story_data.prologue),
            Form(
                hx_post=f"/prologue?id={id}",
                hx_swap="innerHTML",
                hx_target="main",
                hx_indicator="#feedback-loader",
            )(
                Textarea(
                    name="feedback",
                    placeholder="Enter your feedback here...",
                    rows=4,
                    style="width: 100%; margin-bottom: 10px;",
                ),
                Button(type="submit", cls="btn-submit", style="margin-bottom: 10px")(
                    "Change Prologue With Feedback"
                ),
            ),
            Button(
                hx_post=f"/scene?id={id}",
                hx_swap="innerHTML",
                hx_target="main",
                hx_indicator="#feedback-loader",
                cls="btn-submit contrast",
                style="margin-top: 0; width: 100%;",
            )("Accept Prologue & Continue Story"),
        ),
    )


