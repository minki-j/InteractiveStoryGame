from fasthtml.common import *

from app.views.components.header import header_component

def settings_view(session, req, res):
    return (
        Title("Story Sim"),
        header_component(),
        Main(
            cls="container", style="max-width: 800px; margin: 0 auto; padding: 20px;"
        )(P("User id: ", session["user_id"])),
    )
