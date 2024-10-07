import uuid
from app.agents.main_graph import main_graph

from questionnaire import BIG5, PROFILE
import json
thread_id = str(uuid.uuid4())
config = {"configurable": {"thread_id": 10}, "recursion_limit":100}

output = main_graph.invoke(
    {
        "profile": json.dumps(PROFILE, ensure_ascii=True, indent=1),
        "big5": json.dumps(BIG5, ensure_ascii=True, indent=1),
        "genre": "steampunk",
    },
    config,
)
print("First Prologue draft is generated")


# while True:
#     user_feedback = input("Enter a feedback:")
#     if user_feedback == "q":
#         break
#     main_graph.update_state(
#         config,
#         {
#             "user_feedback": user_feedback,
#         },
#         as_node="get_feedback_from_user",
#     )
#     output = main_graph.invoke(None, config)


main_graph.update_state(
        config,
        {
            "is_prologue_completed": True,
        },
        as_node="get_feedback_from_user",
    )
main_graph.invoke(None, config)


while True:
    user_decision = input("Enter a decision:")
    
    if user_decision == "q":
        break
    
    try:
        user_decision = int(user_decision)
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
        continue

    main_graph.update_state(
        config,
        {
            "user_decision": user_decision,
        },
        as_node="get_decision_from_user",
    )



user_feedback_list = [
    "It's too grandiose. I want the prologue to start from a more normal and mundane life. ",
    "Make the main character super poor and miserable. ",
    "I don't get what device that Minki is trying to make. Can you make it more clear? ",
    "Don't mention about Minki's parent's divorce. ",
]

for i, user_feedback in enumerate(user_feedback_list):
    main_graph.update_state(
        config,
        {
            "user_feedback": user_feedback,
        },
        as_node="get_feedback_from_user",
    )
    output = main_graph.invoke(None, config)
    print(f"==>> Completed {i+1} / {len(user_feedback_list)} Feedback")
