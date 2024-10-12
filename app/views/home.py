import uuid

from fasthtml.common import *

from questionnaire import PROFILE, BIG5, ANSWER_OPTIONS, LEVEL_OPTIONS, GENRE_OPTIONS


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


def home_view(req, res):
    return (
        Title("Story Sim"),
        Main(cls="container", style="max-width: 800px; margin: 0 auto; padding: 20px;")(
            A(href="/", style="text-decoration: none; color: inherit;")(
                H1("Welcome to Story Sim")
            ),
            P(
                "Please answer the following questions to generate your personalized story."
            ),
            Form(
                hx_post="init",
                hx_swap="outerHTML",
                hx_target="main",
                hx_target_500="#error_msg",
                hx_indicator=".btn-loader",
                hx_replace_url="true",
            )(
                # Add email input with validation
                Div(cls="form-group")(
                    Label("Email", for_="email", style="font-weight: bold;"),
                    Input(
                        type="email",
                        id="email",
                        name="email",
                        required=True,
                        placeholder="Enter your email",
                        pattern="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                        title="Please enter a valid email address",
                        style="width: 100%; padding: 8px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 4px;",
                        value="qmsoqm2@gmail.com",
                    ),
                ),
                # Genre select
                Div(cls="form-group")(
                    Label("Genre", for_="genre", style="font-weight: bold;"),
                    Select(
                        id="genre",
                        name="genre",
                        required=True,
                        style="width: 100%; padding: 8px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 4px;",
                        oninvalid="this.setCustomValidity('Please select a genre')",
                        onchange="this.setCustomValidity('')",
                    )(
                        *[Option(label, value=value) for value, label in GENRE_OPTIONS]
                    ),
                ),
                # Level select
                Div(cls="form-group")(
                    Label("Level", for_="level", style="font-weight: bold;"),
                    Select(
                        id="level",
                        name="level",
                        required=True,
                        style="width: 100%; padding: 8px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 4px;",
                    )(*[Option(label, value=value) for value, label in LEVEL_OPTIONS]),
                ),
                Div(cls="form-group")(
                    H2(
                        "Personality Questions",
                        cls="section-title",
                        style="font-size: 1.5rem; margin-top: 30px; margin-bottom: 20px;",
                    ),
                    *generate_question_forms(BIG5, "big5"),
                ),
                Div(cls="form-group")(
                    H2(
                        "Profile Questions",
                        cls="section-title",
                        style="font-size: 1.5rem; margin-top: 30px; margin-bottom: 20px;",
                    ),
                    *generate_question_forms(PROFILE, "profile"),
                ),
                Button(
                    type="submit",
                    cls="btn-loader btn-submit",
                )("Generate Story"),
            ),
        ),
        Style(
            """
.question-container {
    margin-bottom: 25px;
    background-color: var(--card-background-color);
    padding: 15px;
    border-radius: 8px;
}

.question-text {
    font-weight: bold;
    margin-bottom: 10px;
}

.radio-group {
    display: flex;
    justify-content: flex-start;
    flex-wrap: wrap;
}

.radio-group label {
    display: flex;
    align-items: center;
    margin-right: 10px;
    margin-bottom: 5px;
    cursor: pointer;
}

.radio-group input[type="radio"] {
    margin-right: 5px;
}

.radio-label {
    font-size: 14px;
}

.btn-submit {
    background-color: var(--primary);
    color: var(--primary-inverse);
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.btn-submit:hover {
    background-color: var(--primary-hover);
}

.response-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    table-layout: fixed;
}

.response-table th, .response-table td {
    text-align: center;
    vertical-align: middle;
    padding: 5px;
    border: 1px solid var(--table-border-color);
    font-size: 0.75rem;
}

.response-table td:first-child {
    text-align: center;
}

.response-table th:nth-child(2) { background-color: var(--color-1); }
.response-table th:nth-child(3) { background-color: var(--color-2); }
.response-table th:nth-child(4) { background-color: var(--color-3); }
.response-table th:nth-child(5) { background-color: var(--color-4); }
.response-table th:nth-child(6) { background-color: var(--color-5); }

@media (prefers-color-scheme: dark) {
    .response-table th:nth-child(2) { background-color: var(--color-1-dark); }
    .response-table th:nth-child(3) { background-color: var(--color-2-dark); }
    .response-table th:nth-child(4) { background-color: var(--color-3-dark); }
    .response-table th:nth-child(5) { background-color: var(--color-4-dark); }
    .response-table th:nth-child(6) { background-color: var(--color-5-dark); }
    .question-container {
        background-color: var(--card-background-color-dark);
    }
}

:root {
    --color-1: #ffcccb;
    --color-2: #ffdab9;
    --color-3: #fffacd;
    --color-4: #e0ffb1;
    --color-5: #b3e0ff;
    --color-1-dark: #664e4e;
    --color-2-dark: #665952;
    --color-3-dark: #66655c;
    --color-4-dark: #5c664a;
    --color-5-dark: #4a5966;
    --primary: #007bff;
    --primary-inverse: #fff;
    --primary-hover: #0056b3;
    --table-border-color: #ddd;
    --card-background-color: #f5f5f5;
    --card-background-color-dark: #333333;
}
"""
        ),
    )
