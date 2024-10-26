import os
import sqlite3
from varname import nameof as n

from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, RemoveMessage

from app.agents.subgraphs.writer_agent.state_schema import WriterAgentState
from app.agents.llm_models import get_chat_model

g = StateGraph(WriterAgentState)
g.add_edge(START, "empty_node")

g.add_node("empty_node", RunnablePassthrough())

g.add_edge("empty_node", END)

os.makedirs("./data/writer_agent_graph_checkpoints", exist_ok=True)
db_path = os.path.join(".", "data", "writer_agent_graph_checkpoints", "checkpoints.sqlite")
conn = sqlite3.connect(db_path, check_same_thread=False)
memory = SqliteSaver(conn)

writer_agent_graph = g.compile(checkpointer=memory)

with open("./app/agents/graph_diagrams/writer_agent_graph.png", "wb") as f:
    f.write(writer_agent_graph.get_graph(xray=10).draw_mermaid_png())
