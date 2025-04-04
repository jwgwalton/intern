from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from src.llms import llm_with_duck_duck_go_tool, duck_duck_go_tool
from src.tools import BasicToolNode


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


tool_node = BasicToolNode(tools=[duck_duck_go_tool])

# Nodes within the graph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("duck_duck_go", tool_node)

# Edges
def route_tools(state: State):
    # Any time the 'chatbot' node runs, either go to 'tools' if it calls a tool, or end the loop if it responds directly.
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    # The following dictionary lets you tell the graph to interpret the condition's outputs as a specific node
    # It defaults to the identity function, but if you
    # want to use a node named something else apart from "tools",
    # You can update the value of the dictionary to something else
    # e.g., "tools": "my_tools"
    {"tools": "duck_duck_go", END: END},
)
graph_builder.add_edge("duck_duck_go", "chatbot")


intern = graph_builder.compile()
