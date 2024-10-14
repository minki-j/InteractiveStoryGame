import json

from fasthtml.common import *
from db import db
from itertools import chain


def all_story_card_view(session, req, res):
    stories = db.t.stories.rows_where("user_id = ?", [session["user_id"]])

    first_story = next(stories, None)
    if first_story is None:
        return Div(cls="no-stories")(
            H2("No stories found"),
            P("You don't have any stories yet. Generate one!"),
        )
    else:
        # Chain the first story back with the rest of the stories
        all_stories = chain([first_story], stories)

        return Div()(
            H2("Continue Reading"),
            Grid(style="grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));")(
                *[
                    A(
                        href=f"/story?id={story["id"]}",
                        cls="card story-card",
                        style="""
                            display: block;
                            text-decoration: none;
                            color: inherit;
                            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        """,
                        onmouseover="this.style.boxShadow='0 8px 16px rgba(0,0,0,0.2)'; this.style.transform='translateY(-5px)';",
                        onmouseout="this.style.boxShadow='0 2px 4px rgba(0,0,0,0.1)'; this.style.transform='translateY(0)';",
                    )(
                        Article()(
                            Header(H3(story["title"])),
                            P(f"{" ".join(story['prologue'].split(' ')[:30])}..."),
                            P(
                                f"scenes: {len(json.loads(story['scenes'])) if story['scenes'] else 0}"
                            ),
                        )
                    )
                    for story in all_stories
                ]
            ),
        )
