import json
from pprint import pprint
from fasthtml.common import *
from app.views.components.error_responses import error_modal

from app.agents.main_graph import main_graph
from questionnaire import PROFILE, BIG5


async def initialize_story(request: Request, id: str):
    print("\n>>> CNTRL initialize_story")

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
    r = main_graph.invoke(
        input={
            "profile": json.dumps(PROFILE, ensure_ascii=True, indent=1),
            "big5": json.dumps(BIG5, ensure_ascii=True, indent=1),
            "genre": "steampunk",
            "level": "HighSchool(Grades10-12/Ages15-18)",
        },
        config={"configurable": {"thread_id": id}, "recursion_limit": 100},
    )
    print(f"\n>>> main_graph returned {r}")
    
    if r:
        # full_route = str(request.url_for("TODO_TODO_TODO"))
        # route = full_route.replace(str(request.base_url), "")
        # return RedirectResponse(url=f"/{route}?id={id}", status_code=303)
        # email = form_data.get("email")
        return Div(cls="container")(
            H1("Story generated"),
            P("Your story has been generated. Check your email for the prologue."),
        )
    else:
        return error_modal("An error happened at generate_plot")
