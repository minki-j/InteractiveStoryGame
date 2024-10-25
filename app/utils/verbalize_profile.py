import json

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.agents.llm_models import get_chat_model

from db import db


def verbalize_profile(user_id, profile_json, big5_json):
    print("\n>>> verbalize_profile")

    user = db.t.users.get(user_id)

    verbalized_profile = user.verbalized_profile
    verbalized_big5 = user.verbalized_big5

    if (
        verbalized_profile == ""
        or verbalized_big5 == ""
        or user.is_profile_updated
    ):  # Verbalize profile and big5 only if any of them is empty or different from the existing ones
        print("===> Verbalizing profile and big5")
        chain = (
            ChatPromptTemplate.from_template(
                """
Convert the following information into normal sentences without any numbered lists or bullet points.

---

Examples 1
Input:
{{"1": {{"question": "My moods change quickly.", "current": "agree", "goal": "disagree"}}, "2": {{"question": "I often prioritize taking care of others over myself.", "current": "strongly disagree", "goal": "neutral"}}, "3": {{"question": "I am a morning person.", "current": "strongly disagree", "goal": "strongly agree"}}}}

Output:
My moods tend to change quickly, and I aspire to achieve a bit more consistency in my emotions.
While I don't prioritize taking care of others over myself most of the time, I aim to find a more balanced approach.
I am definitely not a morning person at all, but I strongly aspire to be one.

Examples 2
Input:
{{"1": {{"question": "What is your name?", "answer": "Minki"}}, "2": {{"question": "How old are you?", "answer": "30"}}, "3": {{"question": "What pronouns do you use??", "answer": "he him"}}}}

Output:
My name is Minki. I am 30 years old. I use he/him pronouns.

---

Now, it's your turn.

{content}

---

Output only the converted sentences, no other text or comments.
            """
            )
            | get_chat_model(temp=0.8)
            | StrOutputParser()
        )

        filtered_profile = {}
        for key, value in json.loads(profile_json).items():
            if value["answer"] != "":
                filtered_profile[key] = value

        filtered_big5 = {}
        for key, value in json.loads(big5_json).items():
            if value["current"] != "" or value["goal"] != "":
                filtered_big5[key] = value

        verbalized_profile, verbalized_big5 = chain.batch(
            [
                {"content": json.dumps(filtered_profile)},
                {"content": json.dumps(filtered_big5)},
            ]
        )
        db.t.users.update(
            pk_values=user_id,
            updates={
                "verbalized_profile": verbalized_profile,
                "verbalized_big5": verbalized_big5,
                "is_profile_updated": False,
            },
        )
        return verbalized_profile, verbalized_big5
    else:
        print("===> Skip. No changes in profile or big5")
        return verbalized_profile, verbalized_big5
