import os
from varname import nameof as n
import asyncio

import sqlite3

from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver

from langchain_core.runnables import RunnablePassthrough

from app.agents.state_schema import OverallState, OutputState

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
from app.agents.llm_models import get_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, RemoveMessage
from langchain_core.runnables import RunnableParallel

from app.agents.subgraphs.decision_game.graph import decision_game_graph


def generate_or_edit_prologue(state: OverallState):
    print("\n>>> NODE: generate_or_edit_prologue")

    delete_messages = []

    if state.prologue == "":
        prompt_for_new_prologue = ChatPromptTemplate.from_template(
            """
You are a celebrated {genre} writer known for your extraordinary ability to weave enchanting and immersive tales. In this task, your goal is to craft an prologue for a {genre} story that is 100 words or less. However, there’s a unique twist: you will create the main character based on the reader's profile. While you can exercise creative freedom in developing the character, ensure they remain relatable so the reader can see themselves in this role.

---

**Reader's level**: {level}

---

**Reader Profile**: {profile}

---

**Reader's Personality**: {big5}

---

**Guidelines to Follow**:

1. **Character Development**: Base the character's traits, motivations, and challenges on the reader's profile and personality test results. Aim for depth and nuance to evoke emotional resonance.

2. **Engaging Narrative**: The prologue should be a compelling conclusion to the story, wrapping up loose ends while leaving readers with a sense of wonder or reflection. Incorporate elements of magic, adventure, or personal growth relevant to the character.

3. **Genre**: The story should be a {genre} story.

4. **Level**: The vocabulary of the story should be appropriate for {level}.

5. **Word Count**: The prologue should be 100 words or less.

6. **Output**: Only return the prologue, no other text or comments such as "Here is the prologue: " or "The prologue is ".
"""
        )
        prompt = prompt_for_new_prologue.invoke(
            {
                "genre": state.genre.replace("_", " "),
                "profile": state.profile,
                "big5": state.big5,
                "level": state.level,
            },
        )
    else:
        if len(state.messages) >= 9:
            summary_prompt = "Distill the above chat messages into a single summary message.Focus on what feedback the user gave and how the AI applied to it. Don't need to summarize the whole story."
            summary_message = get_chat_model().invoke(
                state.messages + [HumanMessage(content=summary_prompt)]
            )
            summary_message.content = (
                "The original messages were too long, so summarized as follows: "
                + summary_message.content
            )
            delete_messages.extend(
                [RemoveMessage(id=m.id) for m in state.messages[1:-1]]
            )  # Keep the first(system message) and last message(the last generated prologue)

        previous_messages = (
            [state.messages[0], summary_message, state.messages[-1]]
            if len(delete_messages) > 0
            else state.messages
        )

        prompt_for_editing_prologue = ChatPromptTemplate.from_messages(
            [
                *previous_messages,
                (
                    "user",
                    """
I've enjoyed the story, but have some feedback on the prologue. Please edit the prologue based on the feedback. Only return the prologue, no other text or comments such as "Here is the prologue: " or "The prologue is ".

Feedback: {feedback}""",
                ),
            ]
        )

        prompt = prompt_for_editing_prologue.invoke(
            {
                "feedback": state.prologue_feedback,
            },
        )

    response = get_chat_model().invoke(prompt)

    parser = StrOutputParser()

    return {
        "prologue": parser.invoke(response),
        "messages": delete_messages + prompt.to_messages() + [response],
    }  # prompt.to_messages() contains the first and last messages that are not deleted but it doesn't matter because LangGraph will match the ids and ignore them.

def generate_title(state: OverallState):
    print("\n>>> NODE: generate_title")

    chain = (
        ChatPromptTemplate.from_template(
            """
Write a **creative and unique** title of a story based on the following prologue:

{prologue}

---

Output only the title, no other text or comments. Don't use markdown format or prefix like "Title: " or "The title is ".
            """
        )
    ) | get_chat_model(temp=1.0) | StrOutputParser()

    return {
        "title": chain.invoke(state.prologue),
    }

def check_if_prologue_completed(state: OverallState):
    print("\n>>> CONDITIONAL EDGE: check_if_prologue_completed")
    if state.is_prologue_completed:
        return n(decision_game_graph)
    else:
        return n(generate_or_edit_prologue)


g = StateGraph(input=OverallState, output=OutputState)
g.add_edge(START, n(check_if_prologue_completed))

g.add_node(n(check_if_prologue_completed), RunnablePassthrough())
g.add_conditional_edges(
    n(check_if_prologue_completed),
    check_if_prologue_completed,
    [n(decision_game_graph), n(generate_or_edit_prologue)],
)

g.add_node(generate_or_edit_prologue)
g.add_edge(n(generate_or_edit_prologue), n(generate_title))

g.add_node(generate_title)
g.add_edge(n(generate_title), "get_feedback_from_user")

g.add_node("get_feedback_from_user", RunnablePassthrough())
g.add_edge("get_feedback_from_user", n(check_if_prologue_completed))

g.add_node(n(decision_game_graph), decision_game_graph)
g.add_edge(n(decision_game_graph), "check_if_story_completed")

g.add_node("check_if_story_completed", RunnablePassthrough())
g.add_conditional_edges(
    "check_if_story_completed",
    lambda state: (
        END if state.is_story_completed else n(check_if_prologue_completed)
    ),
    [END, n(check_if_prologue_completed)],
)

os.makedirs("./data/graph_checkpoints", exist_ok=True)
db_path = os.path.join(".", "data", "graph_checkpoints", "checkpoints.sqlite")
conn = sqlite3.connect(db_path, check_same_thread=False)
memory = SqliteSaver(conn)

main_graph = g.compile(checkpointer=memory, interrupt_before=["get_feedback_from_user"])

with open("./app/agents/graph_diagrams/main_graph.png", "wb") as f:
    f.write(main_graph.get_graph(xray=10).draw_mermaid_png())
