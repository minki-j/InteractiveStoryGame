import uuid

from fasthtml.common import *

from questionnaire import PROFILE, BIG5, ANSWER_OPTIONS, LEVEL_OPTIONS, GENRE_OPTIONS

from app.views.components.generate_story_form import generate_story_form
from app.views.components.all_story_card_view import all_story_card_view



def home_view(session, req, res):
    return (
        Title("Story Sim"),
        Header(
            cls="container",
            style="max-width: 800px; margin: 0 auto; padding: 20px; display: flex; justify-content: space-between; align-items: center;",
        )(
            A(href="/", style="text-decoration: none; color: inherit;")(
                H1("Welcome to Story Sim")
            ),
            Div(cls="profile-section")(
                Details(cls="dropdown")(
                    Summary("Profile"),
                    Ul(
                        Li(A(href="/profile")("View Profile")),
                        Li(A(href="/settings")("Settings")),
                        Li(A(href="/logout")("Logout")),
                    ),
                )
            ),
        ),
        Main(cls="container", style="max-width: 800px; margin: 0 auto; padding: 20px;")(
            generate_story_form(session, req, res),
            all_story_card_view(session, req, res),
        ),
    )
