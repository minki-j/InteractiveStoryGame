from fasthtml.common import *
from questionnaire import ANSWER_OPTIONS, PROFILE, BIG5
from db import db
import json


def profile_view(session, req, res):
    user_id = session["user_id"]
    user_data = db.t.users.get(user_id)

    if not user_data.profile:
        user_data.profile = json.dumps(PROFILE)
        db.t.users.update(
            pk_values=user_id,
            updates={"profile": json.dumps(PROFILE)},
        )
    if not user_data.big5:
        user_data.big5 = json.dumps(BIG5)
        db.t.users.update(
            pk_values=user_id,
            updates={"big5": json.dumps(BIG5)},
        )

    profile_data = json.loads(user_data.profile)
    big5_data = json.loads(user_data.big5)

    def generate_question_forms(questions, question_type):
        if question_type == "profile":
            return [
                Div(
                    P(q_data["question"]),
                    Input(
                        type="text",
                        name=f"profile_{q_id}",
                        required=True,
                        value=q_data["answer"],
                        hx_post=f"/update_profile",
                        hx_trigger="change",
                        hx_target="body",
                        hx_swap="none",
                    ),
                )
                for q_id, q_data in questions.items()
            ]
        elif question_type == "big5":
            return [
                Div(cls="question-container")(
                    P(q_data["question"], cls="question-text"),
                    Table(
                        cls="response-table",
                    )(
                        Tr(
                            Th(""),
                            *[
                                Th(option, cls="response-option")
                                for option in ANSWER_OPTIONS
                            ],
                        ),
                        Tr(
                            Td("My current self"),
                            *[
                                Td(
                                    Input(
                                        type="radio",
                                        name=f"big5_current_{q_id}",
                                        value=option,
                                        required=True,
                                        checked=q_data["current"] == option,
                                        hx_post=f"/update_profile",
                                        hx_trigger="change",
                                        hx_target="body",
                                        hx_swap="none",
                                    )
                                )
                                for option in ANSWER_OPTIONS
                            ],
                        ),
                        Tr(
                            Td("I want to become"),
                            *[
                                Td(
                                    Input(
                                        type="radio",
                                        name=f"big5_goal_{q_id}",
                                        value=option,
                                        required=True,
                                        checked=q_data["goal"] == option,
                                        hx_post=f"/update_profile",
                                        hx_trigger="change",
                                        hx_target="body",
                                        hx_swap="none",
                                    )
                                )
                                for option in ANSWER_OPTIONS
                            ],
                        ),
                    ),
                )
                for q_id, q_data in questions.items()
            ]

    return (
        Title("Profile"),
        Header(
            Div(
                cls="container",
                style="display: flex; justify-content: space-between; align-items: center;",
            )(
                A(href="/")(
                    Button(type="submit", cls="outline", style="padding: 0.25rem 0.75rem;")("< Back")
                ),
                H1("Your Profile"),
            )
        ),
        Main(cls="container")(
            Div(id="profile-form")(
                *generate_question_forms(profile_data, "profile"),
                *generate_question_forms(big5_data, "big5"),
                A(href="/")(
                    Button(type="submit", cls="btn-loader btn-submit")("Finish")
                ),
            ),
        ),
    )
