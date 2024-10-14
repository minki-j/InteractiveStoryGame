import json
import uuid
from pprint import pprint
from fasthtml.common import *
from app.views.components.error_responses import error_modal

from app.agents.main_graph import main_graph
from questionnaire import PROFILE, BIG5

from db import db, Users, Stories

async def initialize_story(session, request: Request):
    print("\n>>> CNTRL initialize_story")
    story_id = str(uuid.uuid4())
    print(f"==>> story id: {story_id}")
    print(f"==>> story genre: {form_data.get('genre')}")
    print(f"==>> story level: {form_data.get('level')}")


    form_data = await request.form()

    for key, value in form_data.items():
        if key.startswith("big5"):
            _, type, id = key.split("_")
            if id not in BIG5:
                return error_modal(f"An error happened at initialize_story\n\n{id} not in BIG5 list")
            BIG5[id][type] = value
        elif key.startswith("profile"):
            id = key.split("_")[-1]
            if id not in PROFILE:
                return error_modal(f"An error happened at initialize_story\n\n{id} not in PROFILE list")
            PROFILE[id]["answer"] = value

    print("\n>>> Invoke main_graph")
    response = main_graph.invoke(
        input={
            "profile": json.dumps(PROFILE, ensure_ascii=True, indent=1),
            "big5": json.dumps(BIG5, ensure_ascii=True, indent=1),
            "genre": form_data.get("genre"),
            "level": form_data.get("level"),
        },
        config={"configurable": {"thread_id": story_id}, "recursion_limit": 100},
    )

    if response:
        # Check if user exists without raising an exception
        

        db.t.stories.insert(
            id=story_id,
            user_id=session["user_id"],
            title="",
            prologue=response["prologue"],
        )
        print(f"\n>>> Story inserted with id: {story_id}")

        return RedirectResponse(url=f"/prologue?id={story_id}", status_code=303)

        return Div(cls="container")(
            H1("Your Adventure Awaits!"),
            P("Congratulations! Your personalized story has been successfully generated."),
            Ul(
                Li("A prologue has been sent to your email. Please check your inbox."),
                Li("The full story will be delivered to your email when you make choices from the story."),
                Li("Don't forget to check your spam folder if you can't find the email.")
            ),
            P(cls="mt-4 text-muted")("Having trouble? Contact support at qmsoqm2@gmail.com")
        )
    else:
        return error_modal("An error happened at generate_plot")
