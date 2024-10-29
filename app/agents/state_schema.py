import uuid
from typing import Annotated, List, Literal
from pydantic import BaseModel, Field
from langgraph.graph.message import AnyMessage, add_messages

from questionnaire import LEVELS

# ===========================================
#                VARIABLE SCHEMA
# ===========================================


class Choice(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    chosen: bool = False
    title: str = Field(default="")
    content: str = Field(default="")


class Scene(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str
    choices: List[Choice]
    completed_scene: str = Field(default="")


# ===========================================
#                REDUCER FUNCTIONS
# ===========================================

#! This reducer function is called for 6 times at NODE: let_the_reader_decide
def update_story(original: List[Scene], new: List[Scene]):
    # print(f">>>>> update_story original: {len(original)} new: {len(new)}")

    # print(">>>>> original")
    # for scene in original:
    #     print(scene.id)
    #     print(scene.question[:30])

    # print(">>>>> new")
    # for scene in new:
    #     print(scene.id)
    #     print(scene.question[:30])

    if len(original) == 0:
        return new

    for scene in new:
        found = False
        for original_scene in original:
            if scene.id == original_scene.id:
                original_scene.question = scene.question
                original_scene.choices = scene.choices
                original_scene.completed_scene = scene.completed_scene
                found = True
                break
        if not found:
            original.append(scene)

    # print(f">>>>> updated story: {len(original)}")
    # for scene in original:
    #     print(scene.id)
    #     print(scene.question[:30])

    # print("\n\n")

    return original


# ===========================================
#                    STATE
# ===========================================
class InputState(BaseModel):
    profile: str = Field(default="")
    big5: str = Field(default="")
    genre: str
    level: LEVELS



class OutputState(BaseModel):
    title: str = Field(default="")
    prologue: str = Field(default="")
    current_scene_index: int = Field(default=0)
    story: Annotated[List[Scene], update_story] = Field(default_factory=lambda: [])


class OverallState(InputState, OutputState):
    # Ephemeral Variables
    # MUST be RESET after each loop
    iteration_count: int = 0
    prologue_feedback: str = ""
    is_prologue_completed: bool = False
    is_story_completed: bool = False
    use_agent: bool = False

    # Short Term Memory
    # MAY be UPDATED after each loop

    # Long Term Memory
    messages: Annotated[list[AnyMessage], add_messages]
