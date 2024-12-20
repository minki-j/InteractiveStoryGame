import json

from fasthtml.common import *

from db import db, Scene

from app.views.components.header import header_component
def story_view(req, res, id: str):
    print("\n>>> VIEW story_view")

    story_data = db.t.stories.get(id)

    if not story_data:
        raise Exception(f"Story data not found for story_id: {id}")

    if story_data.scenes is None:
        print("===> No scenes found, redirecting to prologue")
        return RedirectResponse("/prologue?id=" + id)

    scenes = json.loads(story_data.scenes)
    previous_scene = Scene(**scenes[-2]) if len(scenes) > 1 else None
    current_scene = Scene(**scenes[-1])

    return (
        Title("Story Sim"),
        header_component(),
        Main(cls="container", style="max-width: 800px; margin: 0 auto; padding: 20px;")(
            Details(
                style="""
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 20px;
            """,
            )(
                Summary(style="font-weight: bold;")("Prologue"),
                Article(cls="prologue")(P(cls="marked")(story_data.prologue)),
            ),
            Details(
                style="""
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 20px;
            """,
            )(
                Summary(style="font-weight: bold;")("Previous Scenes"),
                Article(cls="previous-scenes")(
                    *(
                        [
                            P(cls="marked", style="font-weight: bold;")(
                                Scene(**scene).question
                                + "\n\n"
                                + Scene(**scene).completed_scene
                            )
                            for scene in scenes[:-2]
                        ]
                        + [
                            P(cls="marked", style="font-weight: bold;")(
                                Scene(**scenes[-2]).question
                            )
                        ]
                        if len(scenes) >= 2
                        else []
                    ),
                ),
            ),
            P(cls="marked")(previous_scene.completed_scene) if previous_scene else None,
            P(cls="marked")(current_scene.question),
            Form(
                id="choice-form",
                hx_post=f"/scene?id={id}",
                hx_swap="outerHTML",
                hx_target="body",
                hx_indicator=".btn-loader",
            )(
                Div(
                    style="display: flex; flex-direction: column; gap: 3px; margin-bottom: 1rem;",
                )(
                    *[
                        Button(
                            type="submit",
                            cls="btn-loader outline",
                            style="margin-bottom: 0.5rem;",
                            name="chosen_option_index",
                            value=str(i),
                        )(choice.title)
                        for i, choice in enumerate(current_scene.choices)
                    ],
                    Input(
                        type="text",
                        name="custom_user_choice",
                        placeholder="Type your own choice here...",
                        autocomplete="off",
                        style="""
                            flex-grow: 1;
                            margin-bottom: 0.5rem;
                            padding: 10px;
                            border: 1px solid #ccc;
                            border-radius: 4px;
                            text-align: center;
                            cursor: text;
                        """,
                        onkeypress="if(event.key === 'Enter') { event.preventDefault(); htmx.trigger('#choice-form', 'submit'); this.disabled = true;}",
                        onfocus="document.getElementById('submit-message').style.display = 'block';",
                        onblur="document.getElementById('submit-message').style.display = 'none';",
                    ),
                    P(
                        id="submit-message",
                        style="display: none; color: gray; font-size: 0.9em; text-align: center;",
                    )("Press Enter (↵) to submit"),
                ),
            ),
            # Button(
            #     hx_get=f"/delete_story?id={id}",
            #     hx_confirm="Are you sure you want to delete this story?",
            #     style="margin-top: 10px; color: var(--pico-h1-color)",
            #     cls="btn-loader secondary",
            # )("Delete"),
        ),
    )
