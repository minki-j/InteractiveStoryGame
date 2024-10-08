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

from app.agents.subgraphs.decision_game.graph import decision_game_graph

def generate_or_edit_prologue(state: OverallState):
    print("\n>>> NODE: generate_or_edit_prologue")

    delete_messages = []

    if state.prologue == "":
        prompt_for_new_prologue = ChatPromptTemplate.from_template(
            """
You are a celebrated {genre} fantasy fiction writer known for your extraordinary ability to weave enchanting and immersive tales. In this task, your goal is to craft an prologue for a fantasy story that is 300 words or less. However, there’s a unique twist: you will create the main character based on the reader's profile. While you can exercise creative freedom in developing the character, ensure they remain relatable so the reader can see themselves in this role.

---

**Reader Profile**: {profile}

---

**Big Five Personality Test Results**: {big5}

---

**Guidelines to Follow**:

1. **Character Development**: Base the character's traits, motivations, and challenges on the reader's profile and personality test results. Aim for depth and nuance to evoke emotional resonance.

2. **Engaging Narrative**: The prologue should be a compelling conclusion to the story, wrapping up loose ends while leaving readers with a sense of wonder or reflection. Incorporate elements of magic, adventure, or personal growth relevant to the character.

3. **Genre**: The story should be a {genre} story.


---

Let your creativity flow as you bring this character to life and conclude their journey in a way that is both satisfying and thought-provoking!"""
        )
        prompt = prompt_for_new_prologue.invoke(
            {
                "genre": state.genre,
                "profile": state.profile,
                "big5": state.big5,
            },
        )
    else:
        if len(state.messages) >= 9:
            summary_prompt = "Distill the above chat messages into a single summary message.Focus on what feedback the user gave and how the AI applied to it. Don't need to summarize the whole story."
            summary_message = chat_model_small.invoke(
                state.messages + [HumanMessage(content=summary_prompt)]
            )
            summary_message.content = (
                "The original messages were too long, so summarized as follows: "
                + summary_message.content
            )
            delete_messages.extend(
                [RemoveMessage(id=m.id) for m in state.messages[1:-1]]
            ) # Keep the first(system message) and last message(the last generated prologue)

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
I've enjoyed the story, but have some feedback on the prologue. Please edit the prologue based on the feedback.

---

**Feedback**: {feedback}""",
                ),
            ]
        )

        prompt = prompt_for_editing_prologue.invoke(
            {
                "feedback": state.user_feedback,
            },
        )

    response = chat_model_small.invoke(prompt)

    parser = StrOutputParser()

    return {
        "prologue": parser.invoke(response),
        "messages": delete_messages + prompt.to_messages() + [response],
    }  # prompt.to_messages() contains the first and last messages that are not deleted but it doesn't matter because LangGraph will match the ids and ignore them. 


def router(state: OverallState):
    if state.is_prologue_completed:
        return n(decision_game_graph)
    else:
        return n(generate_or_edit_prologue)

g = StateGraph(input=OverallState, output=OutputState)
g.add_edge(START, "is_prologue_done")

g.add_node("is_prologue_done", RunnablePassthrough())
g.add_conditional_edges("is_prologue_done", router, [n(decision_game_graph), n(generate_or_edit_prologue)])

g.add_node(generate_or_edit_prologue)
g.add_edge(n(generate_or_edit_prologue), "get_feedback_from_user")

g.add_node("get_feedback_from_user", RunnablePassthrough())
g.add_edge("get_feedback_from_user", "is_prologue_done")

g.add_node(n(decision_game_graph), decision_game_graph)
g.add_edge(n(decision_game_graph), "check_if_story_completed")

g.add_node("check_if_story_completed", RunnablePassthrough())
g.add_conditional_edges(
    "check_if_story_completed",
    lambda state: END if state.is_story_completed else n(decision_game_graph),
    [END, n(decision_game_graph)]
)

os.makedirs("./data/graph_checkpoints", exist_ok=True)
db_path = os.path.join(".", "data", "graph_checkpoints", "checkpoints.sqlite")
conn = sqlite3.connect(db_path, check_same_thread=False)
memory = SqliteSaver(conn)

main_graph = g.compile(checkpointer=memory, interrupt_before=["get_feedback_from_user"])

with open("./app/agents/graph_diagrams/main_graph.png", "wb") as f:
    f.write(main_graph.get_graph(xray=10).draw_mermaid_png())
