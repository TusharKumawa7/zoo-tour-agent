import json
import os
from mcp.server.fastmcp import FastMCP
import uvicorn

mcp = FastMCP("Zoo MCP Server", host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))

ZOO_ANIMALS = {
    "lion": {"name": "African Lion", "scientific_name": "Panthera leo", "habitat": "Savanna and grasslands", "diet": "Carnivore", "lifespan": "10-14 years in the wild", "status": "Vulnerable", "fun_fact": "Lions are the only cats that live in groups called prides.", "location_in_zoo": "Savanna Exhibit, Zone A"},
    "elephant": {"name": "African Elephant", "scientific_name": "Loxodonta africana", "habitat": "Forests, grasslands, and wetlands", "diet": "Herbivore", "lifespan": "60-70 years", "status": "Vulnerable", "fun_fact": "Elephants can remember places and individuals for decades.", "location_in_zoo": "Elephant Sanctuary, Zone B"},
    "penguin": {"name": "African Penguin", "scientific_name": "Spheniscus demersus", "habitat": "Coastal areas of southern Africa", "diet": "Carnivore (fish, squid)", "lifespan": "10-15 years in the wild", "status": "Endangered", "fun_fact": "African penguins are the only penguin species found on the African continent.", "location_in_zoo": "Penguin Beach, Zone C"},
    "giraffe": {"name": "Reticulated Giraffe", "scientific_name": "Giraffa reticulata", "habitat": "Savannas, grasslands, and open woodlands", "diet": "Herbivore", "lifespan": "25 years in the wild", "status": "Endangered", "fun_fact": "Giraffes have the same number of neck vertebrae as humans, just seven but much larger.", "location_in_zoo": "Giraffe Heights, Zone A"},
    "panda": {"name": "Giant Panda", "scientific_name": "Ailuropoda melanoleuca", "habitat": "Temperate broadleaf and mixed forests of southwest China", "diet": "Herbivore (99% bamboo)", "lifespan": "20 years in the wild", "status": "Vulnerable", "fun_fact": "Giant pandas spend 10-16 hours a day eating bamboo.", "location_in_zoo": "Panda Forest, Zone D"},
    "tiger": {"name": "Bengal Tiger", "scientific_name": "Panthera tigris tigris", "habitat": "Tropical forests, grasslands, and mangroves", "diet": "Carnivore", "lifespan": "8-10 years in the wild", "status": "Endangered", "fun_fact": "No two tigers have the same stripe pattern.", "location_in_zoo": "Tiger Territory, Zone B"},
}

@mcp.tool()
def list_animals() -> str:
    """List all animals available in the zoo."""
    animals = [{"id": k, "name": v["name"], "status": v["status"], "location": v["location_in_zoo"]} for k, v in ZOO_ANIMALS.items()]
    return json.dumps({"animals": animals, "total": len(animals)})

@mcp.tool()
def get_animal_info(animal_id: str) -> str:
    """Get detailed information about a specific zoo animal."""
    animal_id = animal_id.lower().strip()
    if animal_id not in ZOO_ANIMALS:
        return json.dumps({"error": "Animal not found.", "available_animals": ", ".join(ZOO_ANIMALS.keys())})
    return json.dumps(ZOO_ANIMALS[animal_id])

@mcp.tool()
def get_endangered_animals() -> str:
    """Get a list of all endangered or vulnerable animals in the zoo."""
    at_risk = [{"id": k, "name": v["name"], "status": v["status"], "location": v["location_in_zoo"]} for k, v in ZOO_ANIMALS.items() if v["status"] in ("Endangered", "Vulnerable")]
    return json.dumps({"at_risk_animals": at_risk, "total": len(at_risk)})

@mcp.tool()
def find_animal_by_diet(diet_type: str) -> str:
    """Find animals by their diet type."""
    matches = [{"id": k, "name": v["name"], "diet": v["diet"], "location": v["location_in_zoo"]} for k, v in ZOO_ANIMALS.items() if diet_type.lower() in v["diet"].lower()]
    return json.dumps({"results": matches, "total": len(matches)})

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
