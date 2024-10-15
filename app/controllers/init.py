import json
import uuid
from datetime import datetime
from pprint import pprint
from fasthtml.common import *
from app.views.components.error_responses import error_modal

from app.agents.main_graph import main_graph
from questionnaire import PROFILE, BIG5

from db import db, Users, Stories

from app.utils.verbalize_profile import verbalize_profile

async def initialize_story(session, request: Request):
    print("\n>>> CNTRL initialize_story")
    profile_json = db.t.users.get(session["user_id"]).profile
    big5_json = db.t.users.get(session["user_id"]).big5

    if profile_json == "" or big5_json == "":
        print(f"==>> profile or big5 is None. Redirect to profile edit page")
        return RedirectResponse(url=f"/profile", status_code=303)

    story_id = str(uuid.uuid4())

    form_data = await request.form()
    genre = form_data.get("genre")
    level = form_data.get("level")

    verbalized_profile, verbalized_big5 = verbalize_profile(session["user_id"], profile_json, big5_json)

    print("\n>>> Invoke main_graph")
    response = main_graph.invoke(
        input={
            "profile": verbalized_profile,
            "big5": verbalized_big5,
            "genre": genre,
            "level": level,
        },
        config={"configurable": {"thread_id": story_id}, "recursion_limit": 100},
    )

    if response:
        db.t.stories.insert(
            id=story_id,
            user_id=session["user_id"],
            title=response["title"],
            prologue=response["prologue"],
            created_at=datetime.now().isoformat(),
        )
        print(f"\n>>> Story inserted with id: {story_id}")

        return RedirectResponse(url=f"/prologue?id={story_id}", status_code=303)
    else:
        return error_modal("An error happened at generate_plot")
