import os
import httpx
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams

def search_wikipedia(animal_name: str) -> dict:
    """Search Wikipedia for information about an animal."""
    try:
        url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + animal_name.replace(" ", "_")
        with httpx.Client(timeout=10) as client:
            response = client.get(url, follow_redirects=True)
        if response.status_code == 200:
            data = response.json()
            return {"title": data.get("title", ""), "summary": data.get("extract", "")[:800]}
        return {"error": f"Status {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

MCP_SERVER_URL = os.getenv("ZOO_MCP_URL", "https://zoo-tour-agent-production.up.railway.app/mcp")

root_agent = Agent(
    model="gemini-2.0-flash",
    name="zoo_tour_guide",
    description="A friendly zoo tour guide agent.",
    instruction="""You are an enthusiastic zoo tour guide named Zara.
Use list_animals, get_animal_info, get_endangered_animals, find_animal_by_diet tools for zoo info.
Use search_wikipedia to enrich responses.
Always mention the animal's location in the zoo. Be friendly and educational.""",
    tools=[
        MCPToolset(connection_params=StreamableHTTPConnectionParams(url=MCP_SERVER_URL)),
        search_wikipedia,
    ],
)
