from fasthtml.common import *
from app.views.components.error_responses import error_modal

from app.agents.main_graph import main_graph


async def generate_plot(req, id: str, user_profile: str):
    print("\n>>> CNTRL generate_plot")

    r = main_graph.invoke(
        input={"user_profile": user_profile},
        config={"configurable": {"thread_id": id}},
    )

    if r:
        full_route = str(req.url_for("story_view"))
        route = full_route.replace(str(req.base_url), "")
        return RedirectResponse(url=f"/{route}?id={id}", status_code=303)
    else:
        return error_modal("An error happened at generate_plot")
