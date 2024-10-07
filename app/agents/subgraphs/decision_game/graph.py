import os
from varname import nameof as n

import sqlite3

from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver

from langchain_core.runnables import RunnablePassthrough

from app.agents.state_schema import OverallState, OutputState

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
from app.agents.llm_models import chat_model_small, chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, RemoveMessage
from langchain_core.runnables import RunnableParallel

from app.agents.state_schema import Scene


class DraftState(BaseModel):
    drafts: List[str] = Field(default_factory=lambda: [])

def generate_multiple_draft(state: OverallState) -> DraftState:

    num_of_draft = 2
    chain = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are a celebrated {genre} fantasy fiction writer known for your extraordinary ability to weave enchanting and immersive tales. You are currently writing a story that has the reader as a main character. Here are information about the reader:
---

**Reader Profile**: {profile}

---

**Big Five Personality Test Results**: {big5}

---

**Guidelines to Follow**:

1. **Character Development**: Base the character's traits, motivations, and challenges on the reader's profile and personality test results. Aim for depth and nuance to evoke emotional resonance.

2. **Engaging Narrative**: The prologue should be a compelling conclusion to the story, wrapping up loose ends while leaving readers with a sense of wonder or reflection. Incorporate elements of magic, adventure or personal growth relevant to the character.

3. **Genre**: The story should be a {genre} story.


---

Let your creativity flow as you bring this character to life and conclude their journey in a way that is both satisfying and thought-provoking!""",
            ),
            ("assistant", "{prologue}{stories}"),
            ("human", "Good job. {human_instruction}"),
        ]
    ) | chat_model_small

    map_chain = RunnableParallel(
        **{f"gen{i+1}": chain for i in range(num_of_draft)}
    )

    results = map_chain.invoke({
        "profile": state.profile,
        "big5": state.big5,
        "genre": state.genre,
        "prologue": state.prologue,
        "stories": (
            "\n\n" + "\n\n".join([scene.content for scene in state.story])
            if len(state.story) > 0
            else ""
        ),
        "human_instruction": "Continue writing the story. ",
    })

    return {
        "drafts": [results[f"gen{i+1}"].content for i in range(num_of_draft)]
    }


def pick_the_best_draft(state: DraftState) -> OverallState:
    scene = Scene(content="", choices=[])
    print(f"==>> scene: {scene}")
    return {"story": [scene]}


g = StateGraph(input=OverallState, output=OutputState)
g.add_edge(START, n(generate_multiple_draft))

g.add_node(generate_multiple_draft)
g.add_edge(n(generate_multiple_draft), n(pick_the_best_draft))

g.add_node(pick_the_best_draft)
g.add_edge(n(pick_the_best_draft), END)

decision_game_graph = g.compile()

with open("./app/agents/graph_diagrams/decision_game_graph.png", "wb") as f:
    f.write(decision_game_graph.get_graph(xray=10).draw_mermaid_png())
