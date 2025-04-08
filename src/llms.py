from langchain_anthropic import ChatAnthropic
from langchain_community.tools import DuckDuckGoSearchResults


claude = ChatAnthropic(model="claude-3-5-haiku-20241022")


# This means that the GPT-4 will get the details of the tool added to each call so it can decide whether to use it or not in it's response.
duck_duck_go_tool = DuckDuckGoSearchResults(max_results=2)
llm_with_duck_duck_go_tool = claude.bind_tools([duck_duck_go_tool])

