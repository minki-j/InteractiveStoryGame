from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.agents.llm_models import chat_model_small

from db import db


def verbalize_profile(user_id, profile, big5):
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
You are a helpful assistant. Convert the following information into normal sentences without any numbered lists or bullet points.

---

Examples 1
Input:
{{"1": {{"question": "My moods change quickly.", "current": "agree", "goal": "disagree"}}, "2": {{"question": "I often prioritize taking care of others over myself.", "current": "strongly disagree", "goal": "neutral"}}, "3": {{"question": "I am a morning person.", "current": "strongly disagree", "goal": "strongly agree"}}}}

Output:
My moods change quickly but not too much, and I want to be a little bit more consistent. 
I don't prioritize taking care of others over myself almost all the time, but I want to be more balanced.
I am not a morning person at all, but I want to be 100% morning person.

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
            | chat_model_small
            | StrOutputParser()
        )

        verbalized_profile, verbalized_big5 = chain.batch(
            [
                {"content": profile},
                {"content": big5},
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
