import json

from fasthtml.common import *

from db import db, Scene

def story_view(req, res, id: str):
    print("\n>>> VIEW story_view")

    story_data = db.t.stories.get(id)
    scenes = json.loads(story_data.scenes)
    scene = Scene(**scenes[-1])

    if not story_data:
        raise Exception(
            f"Story data not found for story_id: {id}"
        )

    return (
        Title("Story"),
        Main(cls="container")(
            A(href="/", style="text-decoration: none; color: inherit;")(
                H1("Story Sim")
            ),
            P(cls="marked")(scene.question),
            Form(
                hx_post=f"/scene?id={id}",
                hx_swap="outerHTML",
                hx_target="main",
                hx_indicator="#comment-loader",
            )(
                Div(
                    style="display: flex; flex-direction: column; gap: 3px; margin-bottom: 1rem;",
                )(
                    *[
                        Button(
                            type="submit",
                            cls="contrast outline",
                            style="margin-bottom: 0.5rem;",
                            name="chosen_option_index",
                            value=str(i),
                        )(choice.title)
                        for i, choice in enumerate(scene.choices)
                    ]
                ),
            ),
        ),
    )
