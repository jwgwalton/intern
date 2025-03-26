import os

from langchain_openai import AzureChatOpenAI
from langchain_community.tools import DuckDuckGoSearchResults


azure_openai_client = AzureChatOpenAI(
    openai_api_version=os.environ["AZURE_OPENAI_VERSION"],
    openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["AZURE_DEPLOYMENT"],
)


# This means that the GPT-4 will get the details of the tool added to each call so it can decide whether to use it or not in it's response.
duck_duck_go_tool = DuckDuckGoSearchResults(max_results=2)
chat_gpt_with_duck_duck_go_tool = azure_openai_client.bind_tools([duck_duck_go_tool])

