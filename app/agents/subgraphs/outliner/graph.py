import os
from varname import nameof as n
from typing import List, Dict, Any
from pydantic import BaseModel, Field

from langgraph.types import Send
from langgraph.graph import START, END, StateGraph
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

from app.agents.state_schema import OverallState, OutputState, Outline, Character, ChapterOutline
from app.agents.llm_models import chat_model, chat_model_small
from typing import Annotated, TypedDict

from langgraph.graph.message import AnyMessage, add_messages


class RawGeneration(BaseModel):
    content: str


def generate_outline(state: OverallState) -> RawGeneration:
    print("\n>>>> NODE: generate_outline")

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
    # response = chain.invoke(
    #     {
    #         "story_instruction": state.story_instruction,
    #         "user_profile": state.user_profile,
    #     }
    # ).content

    response = """**Title: Perfect Day**

**I. Introduction**

**A. Setting the Scene**
1. Introduction to Minki Jung: A 30-year-old East Asian male living in Montréal, Canada.
2. Description of Minki's appearance and personality: Slim but muscular build, long black curly hair, horn-rimmed glasses, extroverted, empathetic, analytical, curious, enthusiastic, friendly, kind, and confident.
3. Overview of Minki's daily routine: Wakes up at 5:30 AM, meditates, reads for an hour, has breakfast, walks in nature, has coffee, and works for three hours. Lives a disciplined life with his wife Alison and their dog Charlie.

**B. Background and Motivation**
1. Minki's journey from Korea to Canada: Born and raised in Korea, studied physics and philosophy, met his wife Alison in Toronto, immigrated to Canada.
2. Professional background: AI software engineer with a passion for creating a positive impact through AI.
3. Personal goals: To build a successful AI startup called Perfect Day, an app that generates personalized stories with the user as the main character.

**II. The Spark**

**A. The Idea for Perfect Day**
1. Minki's fascination with storytelling and AI: Combining his love for philosophy and AI to create meaningful experiences.
2. The moment of inspiration: During a hike, Minki envisions an app that can craft personalized stories, helping people explore different facets of their lives and make better decisions.

**B. Initial Challenges**
1. Financial constraints: With only $40,000 in the bank, Minki and Alison must be frugal.
2. Lack of resources: No car, no property, and limited access to a network of like-minded engineers.

**III. Building the Foundation**

**A. Research and Development**
1. Minki's analytical approach: Conducting extensive research on AI storytelling, user psychology, and market trends.
2. Initial prototype: Minki spends nights and weekends coding the first version of Perfect Day, balancing his full-time job and startup ambitions.

**B. Support System**
1. Alison's role: As an aspiring writer, Alison provides valuable insights and feedback on the app's storytelling capabilities.
2. Emotional support: Alison's unwavering belief in Minki's vision helps him stay motivated during tough times.

**IV. The First Milestones**

**A. Early Successes**
1. Beta testing: Minki releases a beta version of Perfect Day to a small group of users, receiving positive feedback and constructive criticism.
2. Initial traction: The app starts gaining attention on social media and tech forums, attracting early adopters and potential investors.

**B. Overcoming Obstacles**
1. Technical challenges: Minki faces difficulties in perfecting the AI algorithms to create truly personalized and engaging stories.
2. Balancing life and work: The couple's strict lifestyle and routine are tested as Minki dedicates more time to the startup.

**V. The Turning Point**

**A. Major Breakthrough**
1. Securing funding: Minki pitches Perfect Day to a prominent angel investor, securing the necessary funds to take the app to the next level.
2. Building a team: Minki recruits talented engineers and storytellers who share his vision, moving closer to his goal of making Perfect Day a global success.

**B. Personal Growth**
1. Minki's transformation: Through the ups and downs, Minki learns valuable lessons about resilience, leadership, and the importance of staying true to his values.
2. Strengthening relationships: Despite the challenges, Minki and Alison's bond grows stronger, and they continue to support each other in their respective pursuits.

**VI. The Climax**

**A. Launching Perfect Day**
1. Final preparations: The team works tirelessly to polish the app, ensuring it meets high standards of quality and user experience.
2. The big day: Perfect Day is officially launched, receiving widespread acclaim and quickly gaining a loyal user base.

**B. Facing Competition**
1. Market challenges: As Perfect Day gains popularity, competitors emerge, forcing Minki and his team to innovate and stay ahead of the curve.
2. Ethical dilemmas: Minki grapples with the responsibility of using AI ethically, ensuring the app remains a force for good.

**VII. Resolution**

**A. Achieving Success**
1. Perfect Day's impact: The app becomes a global phenomenon, helping millions of users explore their potential and make better decisions through personalized storytelling.
2. Moving to San Francisco: Minki and Alison relocate to Silicon Valley, further expanding their network and resources.

**B. Reflecting on the Journey**
1. Minki's growth: From a curious and analytical young man to a successful entrepreneur, Minki reflects on the lessons learned and the importance of perseverance and authenticity.
2. Future aspirations: With Perfect Day thriving, Minki sets his sights on new challenges, continuing to push the boundaries of AI and storytelling.

**VIII. Epilogue**

**A. Legacy of Perfect Day**
1. Long-term impact: Perfect Day's success inspires a new generation of entrepreneurs and innovators, emphasizing the importance of empathy, creativity, and ethical AI.
2. Minki's ongoing journey: As Minki continues to evolve and grow, he remains committed to making a positive impact on the world, one story at a time.

**B. Final Reflection**
1. Minki and Alison's future: The couple looks forward to new adventures and challenges, always supporting each other and staying true to their values.
2. The enduring power of storytelling: Minki's journey serves as a testament to the transformative power of stories, both in our personal lives and in the world at large."""

    return {"content": response}


def convert_to_format(state: RawGeneration) -> OverallState:
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "human",
                "Extract the information from the following message and convert it into the format of the Outline\n\n---\n\n{content}",
            ),
        ]
    )
    chain = prompt | chat_model.with_structured_output(Outline)
    # response = chain.invoke({"content": state.content})
    response = Outline(
        characters=[
            Character(
                name='Minki Jung',
                relationship_to_main_character='Main Character',
                description='A 30-year-old East Asian male living in Montréal, Canada. Slim but muscular build, long black curly hair, horn-rimmed glasses, extroverted, empathetic, analytical, curious, enthusiastic, friendly, kind, and confident.'
            ),
            Character(
                name='Alison',
                relationship_to_main_character='Wife',
                description="Minki's wife, an aspiring writer who provides valuable insights and emotional support."
            ),
            Character(
                name='Charlie',
                relationship_to_main_character='Pet',
                description="Minki and Alison's dog."
            )
        ],
        outline=[
            ChapterOutline(
                title='Introduction',
                description="The story begins by introducing Minki Jung, a 30-year-old East Asian male living in Montréal, Canada. Minki is described in detail, highlighting his slim but muscular build, long black curly hair, and horn-rimmed glasses. His personality traits are explored, showcasing him as extroverted, empathetic, analytical, curious, enthusiastic, friendly, kind, and confident. The narrative then gives an overview of Minki's daily routine, which includes waking up at 5:30 AM, meditating, reading for an hour, having breakfast, walking in nature, enjoying coffee, and working for three hours. Minki lives a disciplined life with his wife Alison and their dog Charlie. The background of Minki's journey from Korea to Canada is shared, detailing his upbringing, education in physics and philosophy, and how he met Alison in Toronto before immigrating to Canada. His professional background as an AI software engineer is highlighted, along with his personal goal of building a successful AI startup called Perfect Day, an app designed to generate personalized stories with the user as the main character."
            ),
            ChapterOutline(
                title='The Spark',
                description="Minki's fascination with storytelling and AI leads him to combine his love for philosophy and technology to create meaningful experiences. The moment of inspiration strikes during a hike when Minki envisions an app that can craft personalized stories, helping people explore different facets of their lives and make better decisions. However, he faces initial challenges, including financial constraints with only $40,000 in the bank, and a lack of resources such as no car, no property, and limited access to a network of like-minded engineers."
            ),
            ChapterOutline(
                title='Building the Foundation',
                description="Minki adopts an analytical approach to research and development, conducting extensive research on AI storytelling, user psychology, and market trends. He begins coding the first version of Perfect Day during nights and weekends while balancing his full-time job and startup ambitions. Alison plays a crucial role in this phase, providing valuable insights and feedback on the app's storytelling capabilities as an aspiring writer. Her unwavering belief in Minki's vision offers emotional support, helping him stay motivated during tough times."
            ),
            ChapterOutline(
                title='The First Milestones',
                description="Minki experiences early successes as he releases a beta version of Perfect Day to a small group of users, receiving positive feedback and constructive criticism. The app starts gaining attention on social media and tech forums, attracting early adopters and potential investors. However, he faces obstacles such as technical challenges in perfecting the AI algorithms to create truly personalized and engaging stories, and the couple's strict lifestyle and routine are tested as Minki dedicates more time to the startup."
            ),
            ChapterOutline(
                title='The Turning Point',
                description="A major breakthrough occurs when Minki secures funding by pitching Perfect Day to a prominent angel investor, obtaining the necessary funds to take the app to the next level. He recruits talented engineers and storytellers who share his vision, moving closer to his goal of making Perfect Day a global success. This phase also marks Minki's personal growth, as he learns valuable lessons about resilience, leadership, and the importance of staying true to his values. His relationship with Alison deepens, as they continue to support each other in their pursuits."
            ),
            ChapterOutline(
                title='The Climax',
                description='The climax of the story revolves around the launch of Perfect Day. The team works tirelessly to polish the app, ensuring it meets high standards of quality and user experience. The big day arrives, and Perfect Day is officially launched, receiving widespread acclaim and quickly gaining a loyal user base. However, as the app gains popularity, competitors emerge, forcing Minki and his team to innovate and stay ahead of the curve. Minki grapples with ethical dilemmas regarding the responsibility of using AI ethically, ensuring the app remains a force for good.'
            ),
            ChapterOutline(
                title='Resolution',
                description='Minki achieves success as Perfect Day becomes a global phenomenon, helping millions of users explore their potential and make better decisions through personalized storytelling. Minki and Alison relocate to Silicon Valley to expand their network and resources. Reflecting on his journey, Minki acknowledges his growth from a curious and analytical young man to a successful entrepreneur, emphasizing the lessons learned about perseverance and authenticity. With Perfect Day thriving, he sets his sights on new challenges, continuing to push the boundaries of AI and storytelling.'
            ),
            ChapterOutline(
                title='Epilogue',
                description="The story concludes by examining the legacy of Perfect Day, which inspires a new generation of entrepreneurs and innovators, highlighting the importance of empathy, creativity, and ethical AI. Minki's ongoing journey is portrayed as he remains committed to making a positive impact on the world, one story at a time. The final reflection reveals Minki and Alison's future, as they look forward to new adventures and challenges, always supporting each other and staying true to their values. The enduring power of storytelling is emphasized, showcasing Minki's journey as a testament to the transformative nature of stories in personal lives and the world."
            )
        ],
        background_setting=['Montréal, Canada', 'Silicon Valley, California']
    )

    return {"outline": response}

def router(state: OverallState):
    print("/n>>> EDGE: router")
    return [
        Send(n(examine_each_unit_of_outline), {"unit": unit, "reference": state.user_profile + state.story_instruction})
        for field in state.outline.__annotations__
        for unit in getattr(state.outline, field)
    ]

def convert_unit_to_string(unit: Any):
    string = ""
    for key, _ in unit.__annotations__.items():
        value = getattr(unit, key)
        string += f"{key}: {value}\n"

    return string

def examine_each_unit_of_outline(router_input: Dict[str, Any]):
    if not isinstance(router_input["unit"], str):
        string_unit = convert_unit_to_string(router_input["unit"])
    else:
        string_unit = router_input["unit"]

    class ExamineResult(BaseModel):
        rationale: str
        is_correct: bool
        feedback: str

    class AmendResult(BaseModel):
        content: str

    def router(info):
        examine_result = info["examine_result"]
        unit = info["unit"]
        print("EXAMINE RESULT: ", examine_result.is_correct)
        if examine_result.is_correct:
            print("Return the original unit")
            return unit
        else:
            print("Amend the unit")
            return (
                ChatPromptTemplate.from_template(
                    """
    Amend the unit based on the instruction
                                                **Instruction**: {instruction}
                                                **Unit**: {unit}"""
                ).partial(instruction=examine_result.feedback, unit=unit)
                | chat_model_small.with_structured_output(AmendResult)
            )

    chain1 = (
        ChatPromptTemplate.from_template(
            """
    Check if the following unit of the outline corresponds to the reference.

    **Reference**: {reference}

    **Unit**: {unit}
    """
        )
        | chat_model_small.with_structured_output(ExamineResult)
    )

    chain2 = {
        "unit": lambda x: x["unit"],
        "examine_result": chain1,
    } | RunnableLambda(router)
    result = chain2.invoke({"unit": string_unit, "reference": router_input["reference"]})
    print("RESULT: ", result)
    return result

def return_output_state(state: OverallState) -> OutputState:
    print("\n>>> NODE: return_output_state")
    return {
        "outline": state.outline,
        "chapter_content": state.chapter_content,
    }

g = StateGraph(OverallState)
g.add_edge(START, n(generate_outline))

g.add_node(generate_outline)
g.add_edge(n(generate_outline), n(convert_to_format))

g.add_node(convert_to_format)
g.add_edge(n(convert_to_format), n(router))

g.add_node(n(router), RunnablePassthrough())
g.add_conditional_edges(n(router), router)

g.add_node(examine_each_unit_of_outline)
g.add_edge(n(examine_each_unit_of_outline), "rendevouz")

g.add_node("rendevouz", RunnablePassthrough())
g.add_edge("rendevouz", n(return_output_state))

g.add_node(return_output_state)
g.add_edge(n(return_output_state), END)

outliner_graph = g.compile()

with open("./app/agents/graph_diagrams/outliner_graph.png", "wb") as f:
    f.write(outliner_graph.get_graph(xray=10).draw_mermaid_png())
