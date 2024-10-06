from varname import nameof as n

from langgraph.graph import START, END, StateGraph
from langchain_core.runnables import RunnablePassthrough

from app.agents.state_schema import OverallState, Chapter
from app.agents.llm_models import chat_model_small
from langchain_core.prompts import ChatPromptTemplate


def generate_chapter_content(state: OverallState):
    print(f"\n>>> NODE: generate_chapter_content")
    chain = ChatPromptTemplate.from_template(
        "Write a content of the current chapter with the provided plots and information about the characters and background setting.\n\n---\n\n**Previous plot**: {previous_chapter_plot}\n\n**Current Plot**: {current_chapter_plot}\n\n**Next Plot**: {next_chapter_plot}\n\n**Information**: {information}\n\n---\n\n**Important Conditions that you must follow**\n\n1. Be creative and write in a way that is engaging and interesting to read.\n2. Leave the id as an empty string.\n3. This is not a summary, so it should have dialogue and description and etc."
    ) | chat_model_small.with_structured_output(Chapter)

    chapter = chain.invoke(
        {
            "previous_chapter_plot": state.outline.plots[
                state.current_chapter_num - 2 
            ].model_dump_json(indent=1,exclude={"id"}).replace(r'["{}\s]', '') if state.current_chapter_num > 1 else "No previous chapter",
            "current_chapter_plot": state.outline.plots[
                state.current_chapter_num - 1
            ].model_dump_json(indent=1,exclude={"id"}).replace(r'["{}\s]', ''),
            "next_chapter_plot": state.outline.plots[
                state.current_chapter_num
            ].model_dump_json(indent=1,exclude={"id"}).replace(r'["{}\s]', ''),
            "information": "\n".join(
                [
                    character.model_dump_json(indent=1,exclude={"id"})
                    for character in state.outline.characters
                ]
                + [
                    background_setting.model_dump_json(indent=1,exclude={"id"})
                    for background_setting in state.outline.background_settings
                ]
            ),
        },
    )  # TODO: the information should be curated by a retrieval system.
    chapter.id = state.outline.plots[state.current_chapter_num - 1].id
    return {"chapters": [chapter]}


g = StateGraph(OverallState)
g.add_edge(START, n(generate_chapter_content))

g.add_node(n(generate_chapter_content), generate_chapter_content)
g.add_edge(n(generate_chapter_content), END)

writer_graph = g.compile()

with open("./app/agents/graph_diagrams/writer_graph.png", "wb") as f:
    f.write(writer_graph.get_graph(xray=10).draw_mermaid_png())
