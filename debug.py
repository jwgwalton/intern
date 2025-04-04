import os
import uuid
import tempfile
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


def stream_graph_updates(graph, user_input:str):
    for event in graph.stream({"messages": {"role": "user", "content": user_input}}):
        for value in event.values():
            print(f"Assistant: {value['messages'][-1].content}")


while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    stream_graph_updates(intern, user_input)
