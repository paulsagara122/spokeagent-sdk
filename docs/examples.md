### 📄 `docs/examples.md`

````markdown
# 🔍 Examples: Real-World Usage of SpokeAgent SDK

This document shows real-world examples for using **SpokeAgent SDK** to register agents, obtain secure tokens, and make authenticated API calls. You’ll also learn how to plug the SDK into LangChain tools.

---

## 📘 Example 1: Basic Agent Registration and API Call

```python
from spokeagent_sdk import SpokeAgentClient, SpokeAgentConfig

# Initialize configuration
config = SpokeAgentConfig(
    base_url="https://api.spokeagent.com",
    api_key="your_admin_api_key"
)

client = SpokeAgentClient(config)

# Register an agent
agent = client.register_agent(
    agent_name="summary-bot",
    metadata={"purpose": "generate daily reports"}
)

# Get access token for the agent
token = client.get_token(
    agent_id=agent["id"],
    scopes=["read:reports", "send:email"]
)

# Make a secure API call
response = client.call_api(
    endpoint="/api/reports/today",
    method="GET"
)

print("📊 Today's Report:", response)
````

---

## 🤖 Example 2: LangChain Tool for Secure API Call

```python
from spokeagent_sdk.langchain_wrapper import SpokeAgentTool
from spokeagent_sdk import SpokeAgentConfig

config = SpokeAgentConfig(
    base_url="https://api.spokeagent.com",
    api_key="your_admin_api_key"
)

# Wrap as a LangChain tool
tool = SpokeAgentTool(
    config=config,
    agent_name="langchain-secure-bot",
    scopes=["query:documents"]
).as_tool(
    name="DocQueryTool",
    description="Fetch answers from internal documentation",
    endpoint="/api/docs/query",
    method="POST",
    input_map=lambda text: {"query": text}
)
```

Use in LangChain:

```python
from langchain.agents import initialize_agent
from langchain.llms import OpenAI

llm = OpenAI(temperature=0)

agent = initialize_agent(
    tools=[tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

agent.run("How do I configure multi-tenancy?")
```

---

## 🔁 Example 3: Scoped Agents for Task Separation

You can create multiple agents with different scopes for separation of concerns:

```python
# Agent 1: Fetch data
fetcher = client.register_agent("data-fetcher", metadata={...})
token1 = client.get_token(fetcher["id"], scopes=["read:data"])

# Agent 2: Email sender
emailer = client.register_agent("emailer", metadata={...})
token2 = client.get_token(emailer["id"], scopes=["send:email"])
```

---

## 🛡️ Example 4: Calling Internal APIs Securely

```python
response = client.call_api(
    endpoint="/api/internal/user/profile",
    method="GET"
)
```

Your internal backend will verify the JWT and apply scope-based access rules.

---

## 🧪 Example 5: Mocking in Tests

```python
from unittest.mock import patch

@patch("spokeagent_sdk.client.requests.post")
def test_register_agent(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"id": "test-agent"}
    ...
```

See the full test suite under `/tests/`.

---

## 🔗 Related Docs

* [Getting Started](./getting_started.md)
* [LangChain Integration](./using_with_langchain.md)
* [Authentication Flow](./auth_flow.md)

```
