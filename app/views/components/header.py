from fasthtml.common import *


def header_component():
    return (
        Header(
            cls="container",
            style="max-width: 800px; margin: 0 auto; padding: 20px; display: flex; justify-content: space-between; align-items: center;",
        )(
            A(href="/", style="text-decoration: none;")(
                H1(
                    "Story Sim",
                    style="font-weight: 900; font-size: 2.8rem; color: #4A4A4A; margin: 0; text-transform: uppercase; letter-spacing: 1px;",
                )
            ),
            Div(cls="profile-section")(
                Details(cls="dropdown", style="margin: 0;")(
                    Summary("Profile"),
                    Ul(
                        Li(A(href="/profile")("View Profile")),
                        Li(A(href="/settings")("Settings")),
                        Li(A(href="/logout")("Logout")),
                    ),
                )
            ),
        ),
    )
