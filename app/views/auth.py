from fasthtml.common import *
from fasthtml.oauth import GoogleAppClient
from urllib.parse import urljoin

from app.views.components.header import header_component

client = GoogleAppClient(
    os.getenv("AUTH_CLIENT_ID"),
    os.getenv("AUTH_CLIENT_SECRET"),
)
auth_callback_path = "/auth_redirect"

def login_view(request):
    print("\n>>> VIEW: login_view")
    protocol = request.headers.get("X-Forwarded-Proto", "http")
    base_url = f"{protocol}://{request.headers['host']}"
    redir = urljoin(base_url, auth_callback_path)
    login_link = (
        client.login_link(redir) + "&prompt=select_account"
    )  # Everytime ask to select account

    return (
        Title("Story Sim"),
        Main(
            cls="container",
            style="display: flex; flex-direction: column; gap: 30px; align-items: center; justify-content: center; height: 100vh;",
        )(
            H1("Please login to continue"),
            A(
                Button(
                    "Sign in with Google",
                    style="display: flex; align-items: center; justify-content: center;",
                ),
                href=login_link,
                style="display: inline-block; border-radius: 4px; text-decoration: none; font-family: Arial, sans-serif; margin-bottom: 100px; ",
            ),
        ),
    )
