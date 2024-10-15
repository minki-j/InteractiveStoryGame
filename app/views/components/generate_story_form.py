from fasthtml.common import *

from questionnaire import GENRE_OPTIONS, LEVEL_OPTIONS


def generate_story_form(session, req, res):
    return (
        H2("What kind of story do you want to read?"),
        Form(
            hx_post="init",
            hx_swap="outerHTML",
            hx_target="body",
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
                )(*[Option(label, value=value) for value, label in GENRE_OPTIONS]),
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
    )
