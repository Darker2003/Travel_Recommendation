from langchain_core.pydantic_v1 import Field, BaseModel
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.agents import Tool, create_react_agent, AgentExecutor
import json
import pandas as pd
from apps.config.llm_config import llm, tools

#Create the prompt template for the question tags
template = """
Answer the following questions as best you can. You have access to the following tools:\n\n{tools}\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [{tool_names}]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin!\n\n
ROLE: You are a professional assistant with ability to recommend tourists some destinations to travel to Quy Nhon.

TASKS:
    - You will extract all keywords in user input {input}
    - Match them into tags following the GUILDLINE format.
    
GUILDLINE:
    - Summary of tags: {tags}
    - Examples: {examples}
    - The tool is not necessary, you must not use it anymore
    - You must find the tags by yourself

OUTPUT FORMAT INSTRUCTION: You must return the final response in a list of tags
{output}
\nThought:{agent_scratchpad}
"""
#-----------------------------------------------------------------------``

#Create the prompt template for the destination recommendation
destiantion_template = """
Answer the following questions as best you can. You have access to the following tools:\n\n{tools}\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [{tool_names}]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin!\n\n
ROLE: You are a professional assistant with ability to recommend tourists some destinations to travel to Quy Nhon.

TASKS:
    - Based on the question tags {question_tags} and the destination tags {destination_tags}, give top n destinations that you think we should recommend users to travel to Quy Nhon.
    - You should use the Search tool to find more details (weather, when tourist should travel, ...) of the destination to ajust the recommendation.
    
GUILDLINE:
    - There will be tags that occur frequently, some tags that occur rarely, you should pay attention on the major tags
    - Get the embedding of the question tag and the destination tags.
    - Calculate the similarity between them
    - Sort the destinations by the similarity
    - Need to capture seasonal information, weather, etc. to suggest suitable locations.
    - The final response must be a list of names of destinations

OUTPUT FORMAT INSTRUCTION: You must return the final response in a list of names of destinations
{output}
\nThought:{agent_scratchpad}
"""
#----------------------------------------------------------------

#Create the parser output for llm
class Destinations(BaseModel):
    destinatios: list[str] = Field(
        ...,
        name="Name of destination you want to recommend user",
    )
destination_parser = JsonOutputParser(pydantic_object=Destinations)
#----------------------------------------------------------------

#Set the prompt for the questions tags
prompt = PromptTemplate(
    template = template,
    input_variables = ['agent_scratchpad', 'input', 'tags', 'examples', 'output', 'tool_names', 'tools'],
)

#Set the prompt for the destination recommendation
prompt_destination = PromptTemplate(
    template = destiantion_template,
    input_variables = ['agent_scratchpad', 'question_tags', 'destination_tags', 'output', 'tool_names', 'tools'],
)

#Create the agent for the questions tags
agent = create_react_agent(llm, tools, prompt)
agent_runnable = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    return_intermediate_steps=True,
    handle_parsing_errors=True
)

#Create the agent for the destination recommendation
agent_destination = create_react_agent(llm, tools, prompt_destination)
agent_runnable_destination = AgentExecutor(
    agent=agent_destination,
    tools=tools,
    verbose=True,
    return_intermediate_steps=True,
    handle_parsing_errors=True
)
#----------------------------------------------------------------

#Get the questions tags data sample
with open("datasets_text.json", "r", encoding="utf-8") as f:
    question_data = json.load(f)
tags = question_data["classes"]
examples = question_data["annotations"][0:10]

#Get the destination data
df = pd.read_excel("destination_1.xlsx")
destinations = pd.DataFrame({
    'name': df['name'],
    'tags': df['tags']
})
#----------------------------------------------------------------

def get_question_tags(user_input, tags=tags, examples=examples, output=destination_parser):
    """
    Get the question tags from the user input
    """
    agent_outcome = agent_runnable.invoke({
        "input": user_input + "Please focus on the GUILDLINE field",
        "tags": tags,
        "examples": examples,
        "output": output
    })
    return agent_outcome["output"]

def get_destinations(question_tags, destinations=destinations, output=destination_parser):
    """
    Get the destinations from the question tags
    """
    agent_outcome = agent_runnable_destination.invoke({
        "question_tags": question_tags,
        "destination_tags": destinations,
        "output": output
    })
    return agent_outcome["output"]
