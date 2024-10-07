import uuid
from app.agents.main_graph import main_graph

from questionnaire import BIG5, PROFILE
import json
thread_id = str(uuid.uuid4())
config = {"configurable": {"thread_id": 7}, "recursion_limit":100}

output = main_graph.invoke(
    {
        "profile": json.dumps(PROFILE, ensure_ascii=True, indent=1),
        "big5": json.dumps(BIG5, ensure_ascii=True, indent=1),
        "genre": "steampunk",
    },
    config,
)


# while True:
#     user_feedback = input("Enter a feedback:")
#     main_graph.update_state(
#         config,
#         {
#             "user_feedback": user_feedback,
#         },
#         as_node="get_feedback_from_user",
#     )
#     output = main_graph.invoke(None, config)


user_feedback_list = [
    "It's too grandios. I want the prologue to start from a more normal and mundane life. ",
    "Make the main character super poor and miserable. ",
    "I don't get what device that Minki is trying to make. Can you make it more clear? ",
    "Don't mention about Minki's parent's divorce. ",
]

for i, user_feedback in enumerate(user_feedback_list):
    print(f"==>> Start {i} / {len(user_feedback_list)} Feedback")
    main_graph.update_state(
        config,
        {
            "user_feedback": user_feedback,
        },
        as_node="get_feedback_from_user",
    )
    output = main_graph.invoke(None, config)
