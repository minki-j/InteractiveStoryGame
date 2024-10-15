import json
from fasthtml.common import *
from db import db


async def update_profile(req, session):
    print("\n>>> CNTRL: update_profile")
    form_data = await req.form()
    user_id = session["user_id"]
    user_data = db.t.users.get(user_id)

    profile_data = json.loads(user_data.profile)
    big5_data = json.loads(user_data.big5)

    for key, value in form_data.items():
        print(f"==>> key: {key}, value: {value}")
        if key.startswith("profile_"):
            _, q_id = key.split("_")
            if q_id not in profile_data:
                profile_data[q_id] = {"question": "", "answer": ""}
            profile_data[q_id]["answer"] = value
        elif key.startswith("big5_"):
            _, current_or_goal, q_id = key.split("_")
            if q_id not in big5_data:
                big5_data[q_id] = {"question": "", "current": "", "goal": ""}
            big5_data[q_id][current_or_goal] = value

    db.t.users.update(
        pk_values=user_id,
        updates={
            "profile": json.dumps(profile_data),
            "big5": json.dumps(big5_data),
            "is_profile_updated": True,
        },
    )

    return Response("", 204)
