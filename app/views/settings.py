from fasthtml.common import *


def settings_view(session, req, res):
    return (
        Title("Settings"),
        Main(cls="container", style="max-width: 800px; margin: 0 auto; padding: 20px;")(
            H1("Settings")
        )
    )