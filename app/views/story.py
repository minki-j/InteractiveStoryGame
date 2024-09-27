from fasthtml.common import *

from db import db

def story_view(req, res, id: str):
    print("\n>>> VIEW story_view")
    print(f"ID: {id}")

    story_data = db.t.stories.get(id)
    
    if not story_data:
        raise Exception(
            f"Story data not found for story_id: {id}"
        )
    
    print(f"Story title: {story_data.title}")

    return (
        Title("Story"),
        Main(cls="container")(
            H1(story_data.title),
            P(story_data.content),
        ),
    )

