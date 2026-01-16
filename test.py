import requests

PROM_URL = "http://localhost:9090"

query = "up"
response = requests.get(
    f"{PROM_URL}/api/v1/query",
    params={"query": query}
)

data = response.json()

print("Status:", data["status"])
for result in data["data"]["result"]:
    instance = result["metric"].get("instance", "unknown")
    value = result["value"][1]
    print(f"{instance} -> {value}")