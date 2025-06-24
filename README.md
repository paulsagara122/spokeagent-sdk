````markdown
# 🧠 SpokeAgent SDK for Python

The **SpokeAgent SDK** is a lightweight Python client for integrating with **AuthSpoke’s identity and access management system** built specifically for **autonomous AI agents**.

Securely register AI agents, issue scoped access tokens, and call protected APIs — all in a LangChain-ready interface.

---

## 🚀 Features

- 🔐 Register and authenticate autonomous agents
- 🎯 Issue scoped JWT tokens for secure API access
- ⚙️ Make authenticated API calls on behalf of agents
- 🧩 Seamless integration with [LangChain](https://github.com/langchain-ai/langchain)
- 🧪 Full support for mocking, testing, and CI pipelines

---

## 📦 Installation

Install the required dependencies based on your environment:

### 🔒 Production (SDK usage only)

```bash
pip install -r requirements.txt
````

Includes:

* [`requests`](https://pypi.org/project/requests/) for HTTP communication
* [`langchain`](https://pypi.org/project/langchain/) for optional LangChain integration

---

### 🧪 Development & Testing (SDK contributors)

```bash
pip install -r requirements-dev.txt
```

Includes all production dependencies, plus:

* [`pytest`](https://pypi.org/project/pytest/) — run tests
* [`requests-mock`](https://pypi.org/project/requests-mock/) — mock HTTP APIs
* [`python-dotenv`](https://pypi.org/project/python-dotenv/) — manage `.env` config

---

## 🧑‍💻 Example Usage

```python
from spokeagent_sdk import SpokeAgentClient, SpokeAgentConfig

config = SpokeAgentConfig(
    base_url="https://api.spokeagent.com",
    api_key="your_admin_api_key_here"
)

client = SpokeAgentClient(config)

# Register the agent
agent = client.register_agent("my-langchain-bot", metadata={"purpose": "summarize docs"})

# Get a scoped token
token = client.get_token(agent["id"], scopes=["read:documents"])

# Make an authenticated call
response = client.call_api("/api/documents/today", method="GET")
print(response)
```

---

## 🔗 LangChain Integration

You can easily wrap any SpokeAgent-secured API as a LangChain `Tool`:

```python
from spokeagent_sdk.langchain_wrapper import SpokeAgentTool

tool = SpokeAgentTool(config, agent_name="reporter", scopes=["read:data"]).as_tool(
    name="ReportFetcher",
    description="Fetches today's report",
    endpoint="/api/reports/today",
    method="GET"
)
```

---

## ✅ Running Tests

To run the unit tests:

```bash
pytest tests/
```

Tests are located in the `tests/` folder and use `pytest` and `requests-mock`.

---

## 📁 Project Structure

```
spokeagent_sdk/
├── __init__.py
├── client.py
├── auth.py
├── config.py
├── error.py
├── langchain_wrapper.py
├── utils.py
examples/
├── example_usage.py
tests/
├── test_client.py
├── test_auth.py
├── test_langchain_wrapper.py
├── test_example_usage.py
├── ...
```

---

## 🤝 Contributing

We welcome contributions! Please fork the repo, create a branch, and submit a pull request.

---

## 🏢 Maintained by [AuthSpoke](https://authspoke.com)

AuthSpoke builds secure, extensible identity infrastructure for modern enterprises and AI-native systems.

---

## 📜 License

MIT License

```
