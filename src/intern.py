from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from src.llms import llm_with_duck_duck_go_tool, duck_duck_go_tool


class State(TypedDict):
    # List of all the human & llm  messages, the add_messages operator appends messages to the list
    # this is a reducer annotation, if you don't define one then the default behaviour is to overwrite the value
    messages: Annotated[list, add_messages]


# the StateGraph means that each node can receive the current State as input, and output an update to the state.
graph_builder = StateGraph(State)


def chatbot(state: State):
    llm_response = llm_with_duck_duck_go_tool.invoke(state["messages"])
    # Note the reducer function will append this list of messages to the existing list of messages
    return {"messages": [llm_response]}


tool_node = ToolNode(tools=[duck_duck_go_tool])

# Nodes within the graph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("duck_duck_go", tool_node)

# Edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
    {"tools": "duck_duck_go", END: END},
)
graph_builder.add_edge("duck_duck_go", "chatbot")

# In memory checkpointer
# TODO: Convert this to a sqlite checkpointer
memory = MemorySaver()

intern = graph_builder.compile(checkpointer=memory)
