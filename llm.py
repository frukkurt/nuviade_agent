from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import yaml


load_dotenv()

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_NAME = config["OPENAIMODEL_NAME"]   

llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    temperature=0,
    model=OPENAI_NAME,
)