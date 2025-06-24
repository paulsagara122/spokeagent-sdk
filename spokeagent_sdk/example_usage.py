# Local usage demo (dev only)
from spokeagent_sdk import SpokeAgentClient, SpokeAgentConfig

# 1. Setup config (use environment variables or pass directly)
config = SpokeAgentConfig(
    base_url="https://api.spokeagent.com",     # Replace with your actual API base
    api_key="your_admin_api_key_here"          # Replace with your admin API key
)

# 2. Initialize the client
client = SpokeAgentClient(config)

# 3. Register a new AI agent
try:
    agent = client.register_agent(
        agent_name="langchain-reporter-bot",
        metadata={"purpose": "summarize and email reports"}
    )
    print("✅ Agent registered:", agent)
except Exception as e:
    print("❌ Failed to register agent:", str(e))
    exit()

# 4. Get a scoped token for the agent
try:
    token = client.get_token(agent_id=agent["id"], scopes=["read:reports", "send:email"])
    print("✅ Token acquired:", token)
except Exception as e:
    print("❌ Failed to get token:", str(e))
    exit()

# 5. Make a secure API call with the agent's token
try:
    response = client.call_api(
        endpoint="/api/reports/today",
        method="GET"
    )
    print("📊 Report data:", response)
except Exception as e:
    print("❌ Failed to call API:", str(e))
