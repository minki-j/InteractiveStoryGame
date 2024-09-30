import os
import uuid
import operator
from varname import nameof as n
from typing import List, Dict, Any, Type, Annotated
from pydantic import BaseModel, Field, create_model

from langgraph.types import Send
from langgraph.graph import START, END, StateGraph
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

from app.agents.state_schema import (
    OverallState,
    OutputState,
    Outline,
    Character,
    Plot,
    Unit,
    BackgroundSetting,
)
from app.agents.llm_models import chat_model, chat_model_small

from dotenv import load_dotenv

load_dotenv()

USE_CACHE = os.getenv("USE_CACHE", "False").lower() == "true"
VERIFICATION_ITERATION_COUNT = int(os.getenv("VERIFICATION_ITERATION_COUNT"))


def generate_outline(state: OverallState) -> OverallState:
    print("\n>>> NODE: generate_outline")
    if USE_CACHE:
        return {
            "outline": Outline(
                characters=[
                    Character(
                        id=str(uuid.uuid4()),
                        name="Minki Jung",
                        relationship_to_main_character="Main Character",
                        description="A 30-year-old East Asian male living in Montréal, Canada. Slim but muscular build, short brown hair, metal frame glasses, extroverted, empathetic, analytical, curious, enthusiastic, friendly, kind, and confident.",
                    ),
                    Character(
                        id=str(uuid.uuid4()),
                        name="Alison",
                        relationship_to_main_character="Wife",
                        description="Minki's wife, an aspiring writer who provides valuable insights and emotional support.",
                    ),
                    Character(
                        id=str(uuid.uuid4()),
                        name="Charlie",
                        relationship_to_main_character="Pet",
                        description="Minki and Alison's dog.",
                    ),
                ],
                plots=[
                    Plot(
                        id=str(uuid.uuid4()),
                        title="Introduction",
                        description="The story begins by introducing Minki Jung, a 30-year-old East Asian male living in Montréal, Canada. Minki is described in detail, highlighting his slim but muscular build, long black curly hair, and horn-rimmed glasses. His personality traits are explored, showcasing him as extroverted, empathetic, analytical, curious, enthusiastic, friendly, kind, and confident. The narrative then gives an overview of Minki's daily routine, which includes waking up at 5:30 AM, meditating, reading for an hour, having breakfast, walking in nature, enjoying coffee, and working for three hours. Minki lives a disciplined life with his wife Alison and their dog Charlie. The background of Minki's journey from Korea to Canada is shared, detailing his upbringing, education in physics and philosophy, and how he met Alison in Toronto before immigrating to Canada. His professional background as an AI software engineer is highlighted, along with his personal goal of building a successful AI startup called Perfect Day, an app designed to generate personalized stories with the user as the main character.",
                    ),
                    Plot(
                        id=str(uuid.uuid4()),
                        title="The Spark",
                        description="Minki's fascination with storytelling and AI leads him to combine his love for philosophy and technology to create meaningful experiences. The moment of inspiration strikes during a hike when Minki envisions an app that can craft personalized stories, helping people explore different facets of their lives and make better decisions. However, he faces initial challenges, including financial constraints with only $40,000 in the bank, and a lack of resources such as no car, no property, and limited access to a network of like-minded engineers.",
                    ),
                    Plot(
                        id=str(uuid.uuid4()),
                        title="Building the Foundation",
                        description="Minki adopts an analytical approach to research and development, conducting extensive research on AI storytelling, user psychology, and market trends. He begins coding the first version of Perfect Day during nights and weekends while balancing his full-time job and startup ambitions. Alison plays a crucial role in this phase, providing valuable insights and feedback on the app's storytelling capabilities as an aspiring writer. Her unwavering belief in Minki's vision offers emotional support, helping him stay motivated during tough times.",
                    ),
                    Plot(
                        id=str(uuid.uuid4()),
                        title="The First Milestones",
                        description="Minki experiences early successes as he releases a beta version of Perfect Day to a small group of users, receiving positive feedback and constructive criticism. The app starts gaining attention on social media and tech forums, attracting early adopters and potential investors. However, he faces obstacles such as technical challenges in perfecting the AI algorithms to create truly personalized and engaging stories, and the couple's strict lifestyle and routine are tested as Minki dedicates more time to the startup.",
                    ),
                    Plot(
                        id=str(uuid.uuid4()),
                        title="The Turning Point",
                        description="A major breakthrough occurs when Minki secures funding by pitching Perfect Day to a prominent angel investor, obtaining the necessary funds to take the app to the next level. He recruits talented engineers and storytellers who share his vision, moving closer to his goal of making Perfect Day a global success. This phase also marks Minki's personal growth, as he learns valuable lessons about resilience, leadership, and the importance of staying true to his values. His relationship with Alison deepens, as they continue to support each other in their pursuits.",
                    ),
                    Plot(
                        id=str(uuid.uuid4()),
                        title="The Climax",
                        description="The climax of the story revolves around the launch of Perfect Day. The team works tirelessly to polish the app, ensuring it meets high standards of quality and user experience. The big day arrives, and Perfect Day is officially launched, receiving widespread acclaim and quickly gaining a loyal user base. However, as the app gains popularity, competitors emerge, forcing Minki and his team to innovate and stay ahead of the curve. Minki grapples with ethical dilemmas regarding the responsibility of using AI ethically, ensuring the app remains a force for good.",
                    ),
                    Plot(
                        id=str(uuid.uuid4()),
                        title="Resolution",
                        description="Minki achieves success as Perfect Day becomes a global phenomenon, helping millions of users explore their potential and make better decisions through personalized storytelling. Minki and Alison relocate to Silicon Valley to expand their network and resources. Reflecting on his journey, Minki acknowledges his growth from a curious and analytical young man to a successful entrepreneur, emphasizing the lessons learned about perseverance and authenticity. With Perfect Day thriving, he sets his sights on new challenges, continuing to push the boundaries of AI and storytelling.",
                    ),
                    Plot(
                        id=str(uuid.uuid4()),
                        title="Epilogue",
                        description="The story concludes by examining the legacy of Perfect Day, which inspires a new generation of entrepreneurs and innovators, highlighting the importance of empathy, creativity, and ethical AI. Minki's ongoing journey is portrayed as he remains committed to making a positive impact on the world, one story at a time. The final reflection reveals Minki and Alison's future, as they look forward to new adventures and challenges, always supporting each other and staying true to their values. The enduring power of storytelling is emphasized, showcasing Minki's journey as a testament to the transformative nature of stories in personal lives and the world.",
                    ),
                ],
                background_settings=[
                    BackgroundSetting(
                        id=str(uuid.uuid4()),
                        title="Initial location",
                        content="Montréal, Canada",
                    ),
                    BackgroundSetting(
                        id=str(uuid.uuid4()),
                        title="Where the protagonist is going",
                        content="Silicon Valley, California",
                    ),
                ],
            )
        }

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a famous fiction writer known for your ability to write gripping and interesting stories. You are tasked with writing an outline for a story based on the given story instruction and user profile. Keep in mind that you will then pass this onto a more junior writer to flesh out the outline into a full story, so you should be very detailed in your outline.",
            ),
            (
                "human",
                "Write me a detailed outline of the story based on the following information\n\n---\n\n**story instruction**: {story_instruction}\n**user profile**: {user_profile}",
            ),
        ]
    )

    chain = prompt | chat_model

    raw_content = chain.invoke(
        {
            "story_instruction": state.story_instruction,
            "user_profile": state.user_profile,
        }
    ).content

    prompt2 = ChatPromptTemplate.from_messages(
        [
            (
                "human",
                "Extract the information from the following message and convert it into the format of the Outline. The id fields should be just an empty string and will be filled later.\n\n---\n\n{content}\n\nDon't fortget to leave the id fields empty.",
            ),
        ]
    )

    chain2 = prompt2 | chat_model.with_structured_output(Outline)

    outline = chain2.invoke({"content": raw_content})

    fields = outline.__annotations__
    for field in fields:
        units = getattr(outline, field)
        for unit in units:
            unit.id = str(uuid.uuid4())

    return {"outline": outline}


class PrivateUnitState(BaseModel):
    unit: Unit
    reference: str


def increment_iteration_count(state: OverallState) -> OverallState:
    print(f"\n>>> NODE: increment_iteration_count to {state.iteration_count + 1}")
    return {"iteration_count": state.iteration_count + 1}

def verify_and_edit_unit_in_parallel(state: OverallState) -> List[Send]:
    print("\n>>> EDGE: verify_and_edit_unit_in_parallel")
    return [
        Send(
            n(verify_and_edit_unit),
            PrivateUnitState(
                unit=unit,
                reference=state.user_profile + state.story_instruction,
            ),
        )
        for field in state.outline.__annotations__
        for unit in getattr(state.outline, field)
    ]


def verify_and_edit_unit(state: PrivateUnitState) -> OverallState:
    """
    I combined the verification and editing processes into a single LLM call because editing always requires the same information used for verification.
    For instance, if I first verify whether a unit is correct in one LLM call and then pass the incorrect units for editing in a separate call, I would still need to provide the reference unit and the original (incorrect) unit during the editing step.
    Grouping both tasks streamlines the process, reduce redundancy, and ensure that all necessary information is available at once for both verification and correction.
    """
    print(f">>> NODE: verify_and_edit_unit")

    # convert the unit to a string to use it in the prompt
    if not isinstance(state.unit, str):
        string_unit = ""
        for key, _ in state.unit.__annotations__.items():
            value = getattr(state.unit, key)
            string_unit += f"{key}: {value}\n"
    else:
        string_unit = state.unit

    # dynamically create a Pydantic model for the unit
    class_fields = {
        "rationale": (str, ...),
        "is_correct": (bool, ...),
        "edit_instruction": (
            str,
            Field(
                description="This instruction will be solely used to amend the unit. Be exhaustive in a way that the editing can be done only with this instruction."
            ),
        ),
        "edited_unit": (
            type(state.unit),
            Field(
                description="The edited unit based on the edit instruction. Leave this empty if the unit is correct. Also leave the id field empty."
            ),
        ),
    }
    ExamineResult = create_model("ExamineResult", **class_fields)

    chain = ChatPromptTemplate.from_template(
        "Check if the following unit of the outline corresponds to the reference\n\n---\n\n**Reference**: {reference}\n\n**Unit**: {unit}\n\n---\n\n**Important Conditions that you must follow**\n\n1. If the unit is correct, response edit_instuction and edited_unit with empty string.\n2. When editing, you must leave the id of the unit to an empty string."
    ) | chat_model_small.with_structured_output(ExamineResult)

    verification_result = chain.invoke(
        {"unit": string_unit, "reference": state.reference},
    )  # TODO: the reference should be curated by a retrieval system.

    if verification_result.is_correct:
        return {"outline": []}

    edited_unit = verification_result.edited_unit
    edited_unit.id = state.unit.id
    return {"outline": [edited_unit]}

def iterate_verify_and_edit_unit_until_max_count(state: OverallState):
    print(f"\n>>> EDGE: iterate_verify_and_edit_unit_until_max_count")
    if state.iteration_count >= VERIFICATION_ITERATION_COUNT:
        return END
    else:
        return n(increment_iteration_count)


class PrivateEditUnitState(BaseModel):
    edited_unit: Annotated[List[Unit], operator.add]


g = StateGraph(OverallState)
g.add_edge(START, n(generate_outline))

g.add_node(generate_outline)
g.add_edge(n(generate_outline), n(increment_iteration_count))

g.add_node(n(increment_iteration_count), increment_iteration_count)
g.add_conditional_edges(
    n(increment_iteration_count),
    verify_and_edit_unit_in_parallel,
    path_map=["verify_and_edit_unit"],
)

g.add_node(verify_and_edit_unit)
g.add_edge(n(verify_and_edit_unit), n(iterate_verify_and_edit_unit_until_max_count))

g.add_node(n(iterate_verify_and_edit_unit_until_max_count), RunnablePassthrough())
g.add_conditional_edges(
    n(iterate_verify_and_edit_unit_until_max_count),
    iterate_verify_and_edit_unit_until_max_count,
    path_map=[
        n(increment_iteration_count),
        END,
    ],
)

outliner_graph = g.compile()

with open("./app/agents/graph_diagrams/outliner_graph.png", "wb") as f:
    f.write(outliner_graph.get_graph(xray=10).draw_mermaid_png())
