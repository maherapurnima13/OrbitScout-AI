from pydantic import BaseModel
from typing import List

class AgentTask(BaseModel):
    step: int
    action: str
    target: str

class AgentPlan(BaseModel):
    tasks: List[AgentTask]