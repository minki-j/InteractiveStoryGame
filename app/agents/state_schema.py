import uuid
from typing import Annotated, List
from pydantic import BaseModel, Field
from langgraph.graph.message import AnyMessage, add_messages


# ===========================================
#                VARIABLE SCHEMA
# ===========================================

class Choice(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    chosen: bool = False
    content: str

class Scene(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content: str
    choices: List[Choice]


# ===========================================
#                REDUCER FUNCTIONS
# ===========================================

def update_story(original: List[Scene], new: List[Scene]):
    if len(original) == 0:
        return new
    
    for scene in new:
        for original_scene in original:
            if scene.id == original_scene.id:
                original_scene.title = scene.title
                original_scene.content = scene.content
                original_scene.choices = scene.choices
                break

    return original

# ===========================================
#                    STATE
# ===========================================
class InputState(BaseModel):
    profile: str
    big5: str
    genre: str

class OutputState(BaseModel):
    prologue: str = Field(default="")
    current_scene_index: int = Field(default=0)
    story: Annotated[List[Scene], update_story] = Field(default_factory=lambda: [])

class OverallState(InputState, OutputState):
    # Ephemeral Variables
    # MUST be RESET after each loop
    iteration_count: int = 0
    user_feedback: str = ""

    # Short Term Memory
    # MAY be UPDATED after each loop

    # Long Term Memory
    messages: Annotated[list[AnyMessage], add_messages]
