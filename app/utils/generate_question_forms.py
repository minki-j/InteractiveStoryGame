from fasthtml.common import *

from questionnaire import ANSWER_OPTIONS


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
                ),
            )
            for q_id, q_data in questions.items()
        ]
    elif question_type == "big5":
        return [
            Div(cls="question-container")(
                P(q_data["question"], cls="question-text"),
                Table(cls="response-table")(
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
                                )
                            )
                            for option in ANSWER_OPTIONS
                        ],
                    ),
                ),
            )
            for q_id, q_data in questions.items()
        ]
