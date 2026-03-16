from models import AgentTask, AgentPlan

def create_plan(user_query: str):

    tasks = [
        AgentTask(step=1, action="search_websites", target="aerospace portals"),
        AgentTask(step=2, action="open_pages", target="tender listings"),
        AgentTask(step=3, action="extract_data", target="aerospace tenders"),
        AgentTask(step=4, action="structure_results", target="intelligence report")
    ]

    return AgentPlan(tasks=tasks)