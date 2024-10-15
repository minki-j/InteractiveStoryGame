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
        verbalized_profile is ""
        or verbalized_big5 is ""
        or user.is_profile_updated
    ):  # Verbalize profile and big5 only if any of them is empty or different from the existing ones
        print("===> Verbalizing profile and big5")
        chain = (
            ChatPromptTemplate.from_template(
                """
    You are a helpful assistant. Convert the following information into normal sentences without any numbered lists or bullet points.

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
