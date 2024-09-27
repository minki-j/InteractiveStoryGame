from typing import Annotated, TypedDict

from langgraph.graph.message import AnyMessage, add_messages


class State(TypedDict):
    user_profile: str
    messages: Annotated[list[AnyMessage], add_messages]