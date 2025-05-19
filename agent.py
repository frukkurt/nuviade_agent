from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from demo_tools.list_file_from_googledrive import google_drive_file
from demo_tools.load_sheet_to_polars import google_sheet
from llm import llm
from prompt import prompt_master
import yaml
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)


checkpointer = InMemorySaver()
BASEURL = config["BASEURL"]   
# prompt_master = f"""
#     You are a helpful assistant.

#     Rules
#     1.Answer user same language.
#     2.You can answer all questions that the user asks.
#     3.This is URL for nureva google drive: {BASEURL}.
#     4.You are admin for nureva co.th
#     5. You can use the tools to help you answer the questions.
#     6. Nureva data in nureva google drive
#     """
# Create the agent      
prompt_master_replace = prompt_master.replace("[BASEURL]",BASEURL)
tools_pools = [google_drive_file,google_sheet,]
agent_stateless  = create_react_agent(model=llm, tools=tools_pools, prompt=prompt_master_replace)
agent_stateful  = create_react_agent(model=llm, tools=tools_pools, prompt=prompt_master_replace,checkpointer=checkpointer)