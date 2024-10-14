from fasthtml.common import *
from fasthtml.oauth import GoogleAppClient, redir_url
from db import db

client = GoogleAppClient(
    os.getenv("AUTH_CLIENT_ID"),
    os.getenv("AUTH_CLIENT_SECRET"),
)
auth_callback_path = "/auth_redirect"

def login_view(session, req, res):
    print("\n>>> VIEW: login_view")
    redir = redir_url(req, auth_callback_path)
    redir = "http://localhost:5001/auth_redirect"
    login_link = client.login_link(redir)

    return (
        Title("Login"),
        Main(cls="container")(
            A(href="/", style="text-decoration: none; color: inherit;")(
                H1("Story Sim")
            ),
            P("Please login to continue."),
            A(
                Button(
                    Img(src="/static/google_logo.png", alt="Google logo", style="width: 18px; height: 18px; margin-right: 8px;"),
                    "Sign in with Google",
                    style="display: flex; align-items: center; justify-content: center;"
                ),
                href=login_link,
                style="display: inline-block; padding: 10px 20px; border-radius: 4px; text-decoration: none; font-family: Arial, sans-serif; "
            ),
        ),
    )


