from fasthtml.common import *

from db import db

def story_view(req, res, id: str):
    print("\n>>> VIEW story_view")

    story_data = db.t.stories.get(id)
    
    if not story_data:
        raise Exception(
            f"Story data not found for story_id: {id}"
        )

    return (
        Title("Story"),
        Main(cls="container")(
            H1(story_data.title),
            P(cls="marked")(story_data.scenes[0]),
            Form(
                hx_post="/submit_comment",
                hx_swap="afterend",
                hx_target="this",
                hx_indicator="#comment-loader"
            )(
                
                Button(
                    type="submit",
                    cls="btn-submit"
                )("Submit Comment"),
                Div(id="comment-loader", cls="htmx-indicator")("Submitting..."),
            )
        ),
    )

