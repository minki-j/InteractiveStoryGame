from fasthtml.common import *
from fasthtml.oauth import GoogleAppClient, redir_url
from db import db
import os


client = GoogleAppClient(
    os.getenv("AUTH_CLIENT_ID"),
    os.getenv("AUTH_CLIENT_SECRET"),
)
auth_callback_path = "/auth_redirect"


def auth_redirect(code: str, request, session):
    print("\n>>> CNTRL: auth_redirect")
    redir = redir_url(request, auth_callback_path)
    redir = "http://localhost:5001/auth_redirect"
    user_info = client.retr_info(code, redir)
    user_id = user_info[client.id_key] 
    session["user_id"] = user_id
    print(f"===> user_id: {user_id} saved in session")

    existing_user = next(db.t.users.rows_where("id = ?", [session["user_id"]]), None)
    if existing_user is None:
        db.t.users.insert(
            id=session["user_id"],
            name="",
            email="",
            profile="",
            big5="",
        )
        print(f"===> user inserted in DB with id: {session['user_id']}")

    return RedirectResponse("/", status_code=303)


def logout(session, request, response):
    print("\n>>> CNTRL: logout")
    session.clear()
    print(f"===> session cleared: {session}")
    return RedirectResponse("/", status_code=303)
