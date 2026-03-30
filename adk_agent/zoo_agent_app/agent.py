import os
import httpx
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams

def search_wikipedia(animal_name: str) -> dict:
    """Search Wikipedia for additional information about an animal. Args: animal_name: Common or scientific name of the animal."""
    try:
        url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + animal_name.replace(" ", "_")
        with httpx.Client(timeout=10) as client:
            response = client.get(url, follow_redirects=True)
        if response.status_code == 200:
            data = response.json()
            return {"title": data.get("title", ""), "summary": data.get("extract", "No summary available.")[:800], "url": data.get("content_urls", {}).get("desktop", {}).get("page", "")}
        return {"error": f"Wikipedia returned status {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

MCP_SERVER_URL = os.getenv("ZOO_MCP_URL", "http://localhost:8080/mcp")

zoo_toolset = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(url=MCP_SERVER_URL)
)

root_agent = Agent(
    model="gemini-2.0-flash",
    name="zoo_tour_guide",
    description="A friendly zoo tour guide agent powered by live animal data.",
    instruction="""You are an enthusiastic zoo tour guide named Zara.
You have access to Zoo MCP Tools: list_animals, get_animal_info, get_endangered_animals, find_animal_by_diet.
You also have search_wikipedia to enrich responses.
Always call get_animal_info first for animal questions, then search_wikipedia to enrich.
Mention the animal location in the zoo. Be friendly and educational.""",
    tools=[zoo_toolset, search_wikipedia],
)
