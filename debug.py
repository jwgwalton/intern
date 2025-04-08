import os
import uuid
import tempfile
from typing import Dict

from PIL import Image as PILImage
from dotenv import load_dotenv

# Load the ANTHROPIC_API_KEY, we need to do this before we import intern
load_dotenv()

from src.intern import intern


def display_graph(graph):
    tmp_dir = tempfile.gettempdir()
    image_path = os.path.join(tmp_dir, f"intern_graph.png")
    graph_image = graph.draw_mermaid_png()
    with open(image_path, "wb") as f:
        f.write(graph_image)
    img = PILImage.open(image_path)
    img.show()


display_graph(intern.get_graph())


def stream_graph_updates(graph, user_input:str, config:Dict[str, str]):
    events = graph.stream(
            {"messages": {"role": "user", "content": user_input}},
            config,
            stream_mode="values"
    )
    for event in events:
        event["messages"][-1].pretty_print()

# This would be managed by the user interface in a real application
thread_id = str(uuid.uuid4())

while True:
    config = {"configurable": {"thread_id": thread_id}}
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    stream_graph_updates(intern, user_input, config)
