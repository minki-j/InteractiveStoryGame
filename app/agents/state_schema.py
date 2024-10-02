import operator
from typing import Annotated, TypedDict, List, Dict, Optional, Union
from collections import OrderedDict  # Add this import
import uuid
from pydantic import BaseModel, Field
from langgraph.graph.message import AnyMessage, add_messages


# ===========================================
#                VARIABLE SCHEMA
# ===========================================
class Unit(BaseModel):
    """
    A unit is a smallest atomic component of the outline that is what agents process independently.
    """
    id: str 


class Character(Unit):
    name: str
    relationship_to_main_character: str
    description: str


class Plot(Unit):
    title: str
    description: str = Field(
        description="A detailed synopsis of the chapter in about 500 words. It should have enough detail to be used for story generation."
    )


class BackgroundSetting(Unit):
    title: str
    content: str


class Outline(BaseModel):
    characters: List[Character] = Field(
        description="The characters in the story. Each character has a name and a description."
    )
    plots: List[Plot] = Field(
        description="The top-level outline of the story. Each chapter has a title and a description, which should be as detailed as possible."
    )
    background_settings: List[BackgroundSetting] = Field(
        description="The background setting of the story."
    )

class EditInstruction(BaseModel):
    unit: Unit
    instruction: str


class Chapter(BaseModel):
    id: str
    content: str


# ===========================================
#                REDUCER FUNCTIONS
# ===========================================
def update_outline_unit(original_outline: Outline, new_units: Union[List[Unit], Outline]) -> Outline:
    updated_outline = original_outline.model_copy(deep=True)
    if isinstance(new_units, Outline):
        updated_outline = new_units
    # Update the appropriate list based on the type of new_unit
    for new_unit in new_units:
        if isinstance(new_unit, Character):
            updated_outline.characters = [
                new_unit if unit.id == new_unit.id else unit
                for unit in updated_outline.characters
            ]
        elif isinstance(new_unit, Plot):
            updated_outline.plots = [
                new_unit if unit.id == new_unit.id else unit
                for unit in updated_outline.plots
            ]
        elif isinstance(new_unit, BackgroundSetting):
            updated_outline.background_settings = [
                new_unit if unit.id == new_unit.id else unit
                for unit in updated_outline.background_settings
            ]

    return updated_outline

def update_chapter(original_chapters: List[Chapter], new_chapters: List[Chapter]) -> List[Chapter]:
    updated_chapters = [chapter.model_copy(deep=True) for chapter in original_chapters]
    for new_chapter in new_chapters:
        for idx, chapter in enumerate(updated_chapters):
            if new_chapter.id == chapter.id:
                updated_chapters[idx] = new_chapter
                break
        updated_chapters.append(new_chapter)

    return updated_chapters


# ===========================================
#                    STATE
# ===========================================
class InputState(BaseModel):
    user_profile: str
    story_instruction: str

class OutputState(BaseModel):
    outline: Annotated[Outline, update_outline_unit] = None
    chapters: Annotated[List[Chapter], update_chapter] = None

class OverallState(InputState, OutputState):
    # Ephemeral Variables
    # MUST be RESET after each loop
    iteration_count: int = 0
    user_feedback: str = None
    fields_to_edit: List[str] = None

    # Short Term Memory
    # MAY be UPDATED after each loop
    current_chapter_num: int = 0

    # Long Term Memory
    messages: Annotated[list[AnyMessage], add_messages]
