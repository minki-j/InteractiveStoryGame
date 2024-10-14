from fasthtml.common import *


def settings_view(session, req, res):
    return (
        Title("Settings"),
        Header(
            Div(
                cls="container",
                style="display: flex; justify-content: space-between; align-items: center;",
            )(
                A(href="/")(
                    Button(
                        type="submit", cls="outline", style="padding: 0.25rem 0.75rem;"
                    )("< Back")
                ),
                H1("Settings"),
            ),
        ),
        Main(
            cls="container", style="max-width: 800px; margin: 0 auto; padding: 20px;"
        )(P("User id: ", session["user_id"])),
    )
