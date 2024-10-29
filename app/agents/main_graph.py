import os
import sqlite3
import asyncio
from varname import nameof as n

from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, RemoveMessage
from langchain_core.runnables import RunnableParallel

from app.agents.llm_models import get_chat_model
from app.agents.state_schema import OverallState, OutputState
from app.agents.subgraphs.decision_game.graph import decision_game_graph
from app.agents.subgraphs.writer_agent.graph import writer_agent_graph
from app.agents.prompts import STORY_INSTRUCTION, PROTAGONIST_INFO, GUIDELINES, PROLOGUE_EXTRA_GUIDELINES

def generate_or_edit_prologue(state: OverallState):
    print("\n>>> NODE: generate_or_edit_prologue")

    delete_messages = []

    if state.prologue == "":
        prompt_for_new_prologue = ChatPromptTemplate.from_template(
            STORY_INSTRUCTION.replace("story", "prologue")
            + PROTAGONIST_INFO
            + GUIDELINES
            + PROLOGUE_EXTRA_GUIDELINES
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
I've enjoyed the story, but have some feedback on the prologue. Please edit the prologue based on the feedback. Only return the edited prologue.

Feedback: {feedback}""",
                ),
            ]
        )

        prompt = prompt_for_editing_prologue.invoke(
            {
                "feedback": state.prologue_feedback,
            },
        )

    response = get_chat_model(size="large").invoke(prompt)

    parser = StrOutputParser()

    return {
        "prologue": parser.invoke(response),
        "messages": delete_messages + prompt.to_messages() + [response],
    }  # prompt.to_messages() contains the first and last messages that are not deleted but it doesn't matter because LangGraph will match the ids and ignore them.


def generate_title(state: OverallState):
    print("\n>>> NODE: generate_title")

    chain = (
        (
            ChatPromptTemplate.from_template(
                """
Write a **creative and unique** title of a story based on the following prologue:

{prologue}

---

Output only the title, no other text or comments. Don't use markdown format or prefix like "Title: " or "The title is ".
            """
            )
        )
        | get_chat_model(temp=1.0)
        | StrOutputParser()
    )

    return {
        "title": chain.invoke(state.prologue),
    }


def check_if_prologue_completed(state: OverallState):
    print("\n>>> CONDITIONAL EDGE: check_if_prologue_completed")
    if state.is_prologue_completed:
        return n(check_if_use_agent)
    else:
        return n(generate_or_edit_prologue)


def check_if_use_agent(state: OverallState):
    print("\n>>> CONDITIONAL EDGE: check_if_use_agent")
    if state.use_agent:
        return n(writer_agent_graph)
    else:
        return n(decision_game_graph)


g = StateGraph(input=OverallState, output=OutputState)
g.add_edge(START, n(check_if_prologue_completed))

g.add_node(n(check_if_prologue_completed), RunnablePassthrough())
g.add_conditional_edges(
    n(check_if_prologue_completed),
    check_if_prologue_completed,
    [n(check_if_use_agent), n(generate_or_edit_prologue)],
)

g.add_node(generate_or_edit_prologue)
g.add_edge(n(generate_or_edit_prologue), n(generate_title))

g.add_node(generate_title)
g.add_edge(n(generate_title), "get_feedback_from_user")

g.add_node("get_feedback_from_user", RunnablePassthrough())
g.add_edge("get_feedback_from_user", n(check_if_prologue_completed))

g.add_node(n(check_if_use_agent), RunnablePassthrough())
g.add_conditional_edges(
    n(check_if_use_agent),
    check_if_use_agent,
    [n(decision_game_graph), n(writer_agent_graph)],
)

g.add_node(n(writer_agent_graph), writer_agent_graph)
g.add_edge(n(writer_agent_graph), "check_if_story_completed")

g.add_node(n(decision_game_graph), decision_game_graph)
g.add_edge(n(decision_game_graph), "check_if_story_completed")

g.add_node("check_if_story_completed", RunnablePassthrough())
g.add_conditional_edges(
    "check_if_story_completed",
    lambda state: (END if state.is_story_completed else n(check_if_prologue_completed)),
    [END, n(check_if_prologue_completed)],
)

os.makedirs("./data/graph_checkpoints", exist_ok=True)
db_path = os.path.join(".", "data", "graph_checkpoints", "checkpoints.sqlite")
conn = sqlite3.connect(db_path, check_same_thread=False)
memory = SqliteSaver(conn)

main_graph = g.compile(checkpointer=memory, interrupt_before=["get_feedback_from_user"])

with open("./app/agents/graph_diagrams/main_graph.png", "wb") as f:
    f.write(main_graph.get_graph(xray=10).draw_mermaid_png())
