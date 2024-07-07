from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import GoogleSerperAPIWrapper
import os
from langchain.agents import Tool
from langchain.globals import set_llm_cache
from langchain_community.cache import InMemoryCache

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest",
      google_api_key="",
      temperature=0,
    #   convert_system_message_to_human = True,
      verbose = True,
)
set_llm_cache(InMemoryCache())

os.environ["SERPER_API_KEY"] = "a99dcf55e19000938ce84ce7ecbb0316b134989d"

search = GoogleSerperAPIWrapper()

tools = [
      Tool(
          name = "Search",
          func=search.run,
          description="useful for when you need to answer questions about current events",
      )
        ]