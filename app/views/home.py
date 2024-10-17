from fasthtml.common import *

from app.views.components.generate_story_form import generate_story_form
from app.views.components.all_story_card_view import all_story_card_view
from app.views.components.header import header_component

def home_view(session, req, res):
    return (
        Title("Story Sim"),
        header_component(),        
        Main(cls="container", style="max-width: 800px; margin: 0 auto; padding: 20px;")(
            generate_story_form(session, req, res),
            Div(style="height: 2rem;"),
            all_story_card_view(session, req, res),
        ),
    )
