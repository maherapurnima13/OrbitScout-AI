from fastapi import FastAPI
from pydantic import BaseModel
import asyncio

from fastapi.middleware.cors import CORSMiddleware

from agent import run_agent
from monitoring.scheduler import start_scheduler
from database.service import get_reports


# Initialize FastAPI app
app = FastAPI(
    title="OrbitScout AI",
    description="Autonomous Aerospace Intelligence Agent",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins (good for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Start scheduler when API starts
@app.on_event("startup")
async def startup_event():
    start_scheduler()


# Request model
class Query(BaseModel):
    question: str


# Health route
@app.get("/")
def home():
    return {
        "message": "OrbitScout AI Agent Active"
    }


# Get stored intelligence reports
@app.get("/reports")
def report_history():
    reports = get_reports()
    return reports


# Agent query endpoint
@app.post("/query")
async def query_agent(query: Query):
    """
    Runs the OrbitScout AI agent
    """
    
    result = await run_agent(query.question)

    return result