import asyncio
from planner import create_plan
from tinyfish_agent import run_tinyfish_agent
from crawlers.intelligence import collect_intelligence
from ai.report_engine import generate_intelligence_report


async def run_agent(query):

    plan = create_plan(query)

    intelligence = collect_intelligence()

    report = generate_intelligence_report(intelligence)

    tasks = []

    for step in plan.tasks:

        instruction = f"{step.action} on {step.target}"

        result = await run_tinyfish_agent(instruction)

        tasks.append({
            "step": step.step,
            "instruction": instruction,
            "result": result
        })

    return {
        "query": query,
        "plan": [task.dict() for task in plan.tasks],
        "execution": tasks,
        "aerospace_intelligence": intelligence,
        "intelligence_report": report
    }