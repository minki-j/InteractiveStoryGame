import os
from varname import nameof as n

import sqlite3

from langgraph.graph import START, END, StateGraph
from langchain_core.runnables import RunnablePassthrough
from langgraph.checkpoint.sqlite import SqliteSaver

from app.agents.state_schema import OverallState, OutputState

from app.agents.subgraphs.outliner.graph import outliner_graph
from app.agents.subgraphs.writer.graph import writer_graph


g = StateGraph(input=OverallState, output=OutputState)
g.add_edge(START, n(outliner_graph))

g.add_node(n(outliner_graph), outliner_graph)
g.add_edge(n(outliner_graph), n(writer_graph))

g.add_node(n(writer_graph), writer_graph)
g.add_edge(n(writer_graph), "get_feedback_from_user")

g.add_node("get_feedback_from_user", RunnablePassthrough())
g.add_edge("get_feedback_from_user", n(outliner_graph))

os.makedirs("./data/graph_checkpoints", exist_ok=True)
db_path = os.path.join(".", "data", "graph_checkpoints", "checkpoints.sqlite")
conn = sqlite3.connect(db_path, check_same_thread=False)
memory = SqliteSaver(conn)

main_graph = g.compile(checkpointer=memory, interrupt_before=["get_feedback_from_user"])

with open("./app/agents/graph_diagrams/main_graph.png", "wb") as f:
    f.write(main_graph.get_graph(xray=10).draw_mermaid_png())
