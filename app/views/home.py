import uuid

from fasthtml.common import *

from questionnaire import PROFILE, BIG5, ANSWER_OPTIONS, LEVEL_OPTIONS, GENRE_OPTIONS

def home_view(session, req, res):
    return (
        Title("Story Sim"),
        Main(cls="container", style="max-width: 800px; margin: 0 auto; padding: 20px;")(
            Header(cls="site-header")(
                A(href="/", style="text-decoration: none; color: inherit;")(
                    H1("Welcome to Story Sim")
                ),
                Div(cls="profile-section")(
                    Details(cls="dropdown")(
                        Summary("Profile"),
                        Ul(
                            Li(A(href="/profile")("View Profile")),
                            Li(A(href="/settings")("Settings")),
                            Li(A(href="/logout")("Logout"))
                        )
                    )
                )
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
                # Div(cls="form-group")(
                #     Label("Email", for_="email", style="font-weight: bold;"),
                #     Input(
                #         type="email",
                #         id="email",
                #         name="email",
                #         required=True,
                #         placeholder="Enter your email",
                #         pattern="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                #         title="Please enter a valid email address",
                #         style="width: 100%; padding: 8px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 4px;",
                #         value="qmsoqm2@gmail.com",
                #     ),
                # ),
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
                Div(cls="form-group")(
                    Label("Level", for_="level", style="font-weight: bold;"),
                    Select(
                        id="level",
                        name="level",
                        required=True,
                        style="width: 100%; padding: 8px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 4px;",
                    )(*[Option(label, value=value) for value, label in LEVEL_OPTIONS]),
                ),
                Button(
                    type="submit",
                    cls="btn-loader btn-submit",
                )("Generate Story"),
            ),
        ),
    )
