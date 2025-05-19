from fastapi import FastAPI, Request
from pydantic import BaseModel
from agent import agent_stateless,agent_stateful

app = FastAPI()

class AgentRequest(BaseModel):
    message: str
    thread_id: str = None

@app.post("/ask_thread_id")
async def ask_agent(req: AgentRequest):
    config = {"configurable": {"thread_id": req.thread_id}}
    response = agent_stateful.invoke(
        {"messages": [{"role": "user", "content": req.message}]},
        config=config,
    )
    return {"response": response["messages"][-1].content}

@app.post("/ask")
async def ask_agent(req: AgentRequest):
    response = agent_stateless.invoke(
        {"messages": [{"role": "user", "content": req.message}]},
    )
    return {"response": response["messages"][-1].content}

@app.get("/")
def read_root():
    return {"message": "Nureva Agent API is running"}