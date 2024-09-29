import os
from varname import nameof as n

import sqlite3

from langgraph.graph import START, END, StateGraph
from langchain_core.runnables import RunnablePassthrough
from langgraph.checkpoint.sqlite import SqliteSaver

from app.agents.state_schema import OverallState, OutputState

from app.agents.subgraphs.outliner.graph import outliner_graph


g = StateGraph(input=OverallState, output=OutputState)
g.add_edge(START, n(outliner_graph))

g.add_node("outliner_graph", outliner_graph)
g.add_edge(n(outliner_graph), END)


os.makedirs("./data/graph_checkpoints", exist_ok=True)
db_path = os.path.join(".", "data", "graph_checkpoints", "checkpoints.sqlite")
conn = sqlite3.connect(db_path, check_same_thread=False)
memory = SqliteSaver(conn)

main_graph = g.compile(checkpointer=memory)

with open("./app/agents/graph_diagrams/main_graph.png", "wb") as f:
    f.write(main_graph.get_graph(xray=10).draw_mermaid_png())
