### 📄 `docs/using_with_langchain.md`

````markdown
# 🤖 Using SpokeAgent SDK with LangChain

This guide walks you through integrating **SpokeAgent SDK** with [LangChain](https://github.com/langchain-ai/langchain) to build secure, authenticated tools for your AI agents.

---

## 🔥 Why Use SpokeAgent with LangChain?

| Problem LangChain Devs Face           | How SpokeAgent Helps                              |
|---------------------------------------|---------------------------------------------------|
| APIs need agent-specific authentication | Register agents and issue scoped JWTs           |
| Tools need dynamic, secure auth       | Tools get tokens on demand                      |
| Need auditability of tool actions     | All calls are logged with agent identity        |
| Want granular control over permissions| Use scopes like `read:docs`, `write:email`, etc |

---

## ⚙️ 1. Create a LangChain Tool with Authentication

```python
from spokeagent_sdk import SpokeAgentConfig
from spokeagent_sdk.langchain_wrapper import SpokeAgentTool

# Define config using your API key
config = SpokeAgentConfig(
    base_url="https://api.spokeagent.com",
    api_key="your_admin_api_key"
)

# Create LangChain-compatible tool
tool = SpokeAgentTool(
    config=config,
    agent_name="my-secure-agent",
    scopes=["read:data"]
).as_tool(
    name="SecureDataTool",
    description="Fetches secure data from internal API",
    endpoint="/api/internal/data",
    method="POST"
)
````

---

## 🧠 2. Use Tool in a LangChain Agent

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

agent.run("Get the internal data summary for today")
```

---

## 🔍 3. Input Mapping for LangChain Tools

You can transform input prompts into structured API payloads:

```python
tool = SpokeAgentTool(
    config=config,
    agent_name="my-agent",
    scopes=["query:knowledge"]
).as_tool(
    name="QuestionTool",
    description="Answers knowledgebase queries",
    endpoint="/api/kb/query",
    method="POST",
    input_map=lambda text: {"query": text}
)
```

---

## 🔐 4. Security and Scopes

SpokeAgent issues scoped JWTs for each agent:

```python
# Scopes define access rights
scopes=["read:profile", "generate:summary"]
```

These tokens are automatically injected into every request made by the tool.

---

## ✅ Benefits of Integration

* 🔐 Secure: Agents can't access anything beyond their scopes
* 🔎 Auditable: Track what agent did what and when
* 🔁 Reusable: Wrap any internal API as a LangChain tool
* 🧩 Modular: Plug in multiple tools into your agent

---

## 📎 Example Use Cases

| Tool Name            | Endpoint             | Scope               |
| -------------------- | -------------------- | ------------------- |
| `GenerateReportTool` | `/api/reports/daily` | `read:reports`      |
| `SendSlackTool`      | `/api/notify/slack`  | `send:notification` |
| `QueryDocsTool`      | `/api/docs/query`    | `read:docs`         |

---

## 🧪 Want to Test?

See [../tests/test\_langchain\_wrapper.py](../tests/test_langchain_wrapper.py) for how to test these tools using mocks.

---

## 🔗 Related Docs

* [Getting Started](./getting_started.md)
* [Auth Flow & Token Lifecycle](./auth_flow.md)
* [Examples](./examples.md)

```
