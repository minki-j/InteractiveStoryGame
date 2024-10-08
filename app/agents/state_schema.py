import uuid
from typing import Annotated, List, Literal
from pydantic import BaseModel, Field
from langgraph.graph.message import AnyMessage, add_messages


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
    # title: str
    question: str
    choices: List[Choice]
    completed_scene: str = Field(default="")


# ===========================================
#                REDUCER FUNCTIONS
# ===========================================


def update_story(original: List[Scene], new: List[Scene]):
    if len(original) == 0:
        return new

    for scene in new:
        for original_scene in original:
            if scene.id == original_scene.id:
                # original_scene.title = scene.title
                original_scene.question = scene.question
                original_scene.choices = scene.choices
                break
        original.append(scene)

    return original


# ===========================================
#                    STATE
# ===========================================
class InputState(BaseModel):
    profile: str
    big5: str
    genre: str
    level: Literal[
        "EarlyElementary(Grades1-3/Ages6-9)",
        "UpperElementary(Grades4-6/Ages9-12)",
        "MiddleSchool(Grades7-9/Ages12-15)",
        "HighSchool(Grades10-12/Ages15-18)",
        "UnivFreshman(Ages18-19)",
        "UnivSophomore(Ages19-20)",
        "UnivJunior(Ages20-21)",
        "UnivSenior(Ages21-22)",
        "EmergingProfessionals(Ages22-35)",
        "MatureAdults(Ages35-50)",
        "MidlifeAndBeyond(Ages50-65)",
        "SeniorAdults(Ages65+)",
    ]


class OutputState(BaseModel):
    prologue: str = Field(default="")
    current_scene_index: int = Field(default=0)
    story: Annotated[List[Scene], update_story] = Field(default_factory=lambda: [])


class OverallState(InputState, OutputState):
    # Ephemeral Variables
    # MUST be RESET after each loop
    iteration_count: int = 0
    user_feedback: str = ""
    is_prologue_completed: bool = False
    is_story_completed: bool = False
    # Short Term Memory
    # MAY be UPDATED after each loop

    # Long Term Memory
    messages: Annotated[list[AnyMessage], add_messages]
