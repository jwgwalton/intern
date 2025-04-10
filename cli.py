import os
import uuid
import tempfile
from typing import Dict

from PIL import Image as PILImage
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

# Load the ANTHROPIC_API_KEY, we need to do this before we import intern
load_dotenv()

from src.intern import intern
from src.job_finder import create_job_finder


def display_graph(graph) -> None:
    """
    Displays a graph by generating a temporary image file.

    Args:
        graph: The graph object to display.
    """
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        image_path = temp_file.name
        graph_image = graph.draw_mermaid_png()
        temp_file.write(graph_image)

    img = PILImage.open(image_path)
    img.show()
    os.remove(image_path)


def stream_graph_updates(graph, user_input: str, config: Dict[str, str]) -> None:
    """
    Streams updates to the graph based on user input.

    Args:
        graph: The graph object to stream updates to.
        user_input (str): The input provided by the user.
        config (Dict[str, str]): Configuration dictionary for the graph.
    """
    events = graph.stream(
        {"messages": {"role": "user", "content": user_input}},
        config,
        stream_mode="values"
    )
    for event in events:
        event["messages"][-1].pretty_print()


def main() -> None:
    """
    Main entry point for the application.
    Handles tool selection and user interaction.
    """
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    tool_choice = input("What tool do you wish to work with? ['intern', 'job_hunter']: ").lower()

    if tool_choice == "job_hunter":
        print("Selected job_hunter")
        model = ChatAnthropic(model="claude-3-5-haiku-20241022")
        tool = create_job_finder(model)
    elif tool_choice == "intern":
        print("Selected intern")
        tool = intern
    else:
        print("Invalid choice. Exiting.")
        return

    display_graph(tool.get_graph())

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(tool, user_input, config)


if __name__ == "__main__":
    main()