import operator
from typing_extensions import Literal, Annotated, TypedDict, Dict

from langchain_anthropic import ChatAnthropic
from langchain_community.tools import DuckDuckGoSearchResults
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.types import Command
from langgraph.prebuilt import ToolNode, tools_condition
from src.agent_handoff import make_handoff_tool


def create_job_finder(model: ChatAnthropic):
    """
    This is an agent for finding jobs.
    """

    class JobHunterState(TypedDict):
        messages: Annotated[list[str], operator.add]
        job_results : Annotated[str, operator.add]

    duck_duck_go_tool = DuckDuckGoSearchResults(max_results=2)
    hand_back_to_supervisor_tool = make_handoff_tool(agent_name="supervisor")
    tools = [duck_duck_go_tool, hand_back_to_supervisor_tool]
    model_with_tools = model.bind_tools(tools)

    def find_potential_jobs(state: JobHunterState):
        system_prompt = "You are a job hunter, you will search the internet for contract machine learning engineer jobs and return the results to the user."
        messages = [{"role": "system", "content": system_prompt}] + state["messages"]
        response = model_with_tools.invoke(messages)
        if len(response.tool_calls) > 0:
            return Command(goto="tool_node", update={"messages": [response]})
        return {"messages": [response]}

    def filter_potential_jobs(state: JobHunterState):
        system_prompt = "You are a job hunter, we have searched the internet for contract machine learning engineer jobs. Check the results and see if they are relevant to the user. Return only the relevant results"
        messages = [{"role": "system", "content": system_prompt}] + state["messages"]
        response = model_with_tools.invoke(messages)
        return {"job_results": response.content}


    tool_node = ToolNode(tools=tools)

    graph = StateGraph(JobHunterState)
    graph.add_node(find_potential_jobs)
    graph.add_node(tool_node)
    graph.add_node(filter_potential_jobs)

    graph.add_edge(START, "find_potential_jobs")
    graph.add_edge("find_potential_jobs", "tool_node")
    graph.add_edge("tool_node", "filter_potential_jobs")
    graph.add_edge("filter_potential_jobs", END)

    # What is the flow

    # Call the internet with a relevant query
    # parse the results
    # Check do the results match the query
    # If not, ask the user for more information
    # If yes, return the results back to the supervisor

    return graph.compile()