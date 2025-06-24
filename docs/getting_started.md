### 📄 `docs/getting_started.md`

````markdown
# 🧠 Getting Started with SpokeAgent SDK

Welcome to the **SpokeAgent SDK** — your secure identity and access layer for autonomous AI agents. This guide walks you through setting up the SDK, registering an agent, and securely calling protected APIs in under 10 minutes.

---

## ✅ Prerequisites

- Python 3.8 or higher
- An API key from the [AuthSpoke Dashboard](https://authspoke.com) (or your local test key)

---

## 📦 1. Installation

Install the SDK and its dependencies:

```bash
pip install spokeagent-sdk
````

> Or if you're developing or testing locally:

```bash
pip install -r requirements-dev.txt
```

---

## 🔧 2. Configure the Client

You can create a config object with your API credentials:

```python
from spokeagent_sdk import SpokeAgentConfig

config = SpokeAgentConfig(
    base_url="https://api.spokeagent.com",
    api_key="your_admin_api_key"
)
```

---

## 🤖 3. Register Your AI Agent

Each AI agent (chatbot, RAG model, script) can be registered with a name and metadata.

```python
from spokeagent_sdk import SpokeAgentClient

client = SpokeAgentClient(config)

agent = client.register_agent(
    agent_name="reporting-bot",
    metadata={"purpose": "summarize reports and notify"}
)

print("Agent Registered ✅", agent)
```

---

## 🔑 4. Generate a Scoped Token

Tokens control what the agent can do (e.g., read reports, send emails). This is similar to OAuth scopes.

```python
token = client.get_token(
    agent_id=agent["id"],
    scopes=["read:reports", "send:email"]
)

print("Access Token 🔐", token)
```

---

## 🔗 5. Call a Protected API

Now, make an API request that requires agent-level authentication:

```python
response = client.call_api(
    endpoint="/api/reports/today",
    method="GET"
)

print("📊 Today's Report:", response)
```

---

## 🧩 6. Use with LangChain (Optional)

SpokeAgent provides a LangChain-compatible wrapper for any authenticated API:

```python
from spokeagent_sdk.langchain_wrapper import SpokeAgentTool

tool = SpokeAgentTool(
    config=config,
    agent_name="reporting-bot",
    scopes=["read:reports"]
).as_tool(
    name="FetchReportTool",
    description="Fetches daily report from API",
    endpoint="/api/reports/today",
    method="GET"
)
```

You can now use `tool` in any LangChain agent like `initialize_agent(...)`.

---

## ✅ You're Ready!

You’ve now:

* Configured the SDK
* Registered an agent
* Issued an access token
* Made a secure API call
* Integrated with LangChain (if needed)

---

## 🔗 Next Steps

* [🔗 Using with LangChain](./using_with_langchain.md)
* [🔒 Auth Flow & Token Lifecycle](./auth_flow.md)
* [🧪 Testing the SDK](../tests/)
* [📚 Examples](./examples.md)

For more help or advanced use cases, visit [https://authspoke.com/docs](https://authspoke.com/docs) (coming soon) or reach out to [support@authspoke.com](mailto:support@authspoke.com).

```
