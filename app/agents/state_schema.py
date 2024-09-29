from typing import Annotated, TypedDict, List, Dict, Optional
from collections import OrderedDict  # Add this import

from pydantic import BaseModel, Field
from langgraph.graph.message import AnyMessage, add_messages

class Character(BaseModel):
    name: str
    relationship_to_main_character: str
    description: str


class ChapterOutline(BaseModel):
    title: str
    description: str = Field(
        description="A detailed synopsis of the chapter in about 500 words. It should have enough detail to be used for story generation."
    )


class Outline(BaseModel):
    characters: List[Character] = Field(
        description="The characters in the story. Each character has a name and a description.", default=[]
    )
    outline: List[ChapterOutline] = Field(
        description="The top-level outline of the story. Each chapter has a title and a description, which should be as detailed as possible.",
        default=[]
    )
    background_setting: List[str] = Field(
        description="The background setting of the story.", default=[]
    )

class Chapter(BaseModel):
    chapter_num: int = -1
    chapter_content: str = ""

class OverallState(BaseModel):

    # Inputs
    # CANNOT be changed after initialization

    # Ephemeral Variables
    # MUST be RESET after each loop

    # Short Term Memory
    # MAY be UPDATED after each loop
    current_chapter_num: int = 0  # Default value

    # Long Term Memory
    user_profile: str = ""
    story_instruction: str = ""
    messages: Annotated[list[AnyMessage], add_messages] = []

    # Outputs
    outline: Outline = Field(default=Outline())
    chapter_content: Chapter = Field(default=Chapter())

class OutputState(BaseModel):
    chapter_content: Chapter = Field(default=Chapter())
