from fasthtml.common import *

from db import db
from app.agents.main_graph import main_graph

from app.views.components.header import header_component

def prologue_view(req: Request, id: str):
    print("\n>>> VIEW story_view")

    story_data = db.t.stories.get(id)

    if not story_data:
        raise Exception(f"Story data not found for story_id: {id}")

    return (
        Title("Story Sim"),
        header_component(),
        Main(cls="container", style="max-width: 800px; margin: 0 auto; padding: 20px;")(
            H2(story_data.title),
            P(cls="marked")(story_data.prologue),
            Form(
                hx_post=f"/prologue?id={id}",
                hx_swap="outerHTML",
                hx_target="main",
                hx_indicator=".btn-loader",
                hx_replace_url="true",
            )(
                Textarea(
                    name="feedback",
                    placeholder="Enter your feedback here...",
                    rows=4,
                    style="width: 100%; margin-bottom: 10px;",
                ),
                Button(
                    type="submit",
                    cls="btn-loader",
                    style="margin-bottom: 10px",
                )("Change Prologue With Feedback"),
            ),
            Button(
                hx_post=f"/scene?id={id}",
                hx_swap="outerHTML",
                hx_target="main",
                cls="btn-loader outline",
                style="margin-top: 0; width: 100%;",
            )("Accept Prologue & Continue Story"),
        ),
    )
