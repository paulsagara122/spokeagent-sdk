### 📄 `docs/auth_flow.md`

````markdown
# 🔒 Authentication & Token Lifecycle

This guide explains how the **SpokeAgent SDK** handles authentication, agent registration, and access control using secure JWT tokens.

---

## 🧠 Why Identity for AI Agents?

Autonomous agents (e.g., LangChain, AutoGen, custom Python bots) need identity just like users:

| Challenge                        | SpokeAgent Solution              |
|----------------------------------|----------------------------------|
| Who is this agent calling my API? | Unique agent ID per bot         |
| What is this agent allowed to do? | Scoped JWT token                |
| Can I audit what it accessed?     | Audit logs per agent, per scope |

---

## 🔁 Lifecycle Overview

### 1. **Register Agent**
You define and register an agent (like a service account).

```python
agent = client.register_agent(
    agent_name="summarizer-bot",
    metadata={"purpose": "daily report summarization"}
)
````

* Response: `{ "id": "agent-123", ... }`

---

### 2. **Issue Scoped Token**

Request a token with fine-grained scopes.

```python
token = client.get_token(
    agent_id="agent-123",
    scopes=["read:reports", "write:summary"]
)
```

* Output: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
* Token is short-lived (configurable)
* JWT claims include `agent_id`, `scopes`, `iat`, `exp`

---

### 3. **Call API with Token**

Use the token in authenticated requests.

```python
response = client.call_api(
    endpoint="/api/reports/today",
    method="GET"
)
```

* The SDK injects the `Authorization: Bearer <token>` header
* Your backend verifies and authorizes the call

---

## 🔐 Scope-Based Access Control

Each token is scoped to a set of allowed actions:

| Scope           | Description                       |
| --------------- | --------------------------------- |
| `read:reports`  | Can fetch report data             |
| `write:summary` | Can write new summaries           |
| `send:email`    | Can trigger emails (e.g., alerts) |
| `query:kb`      | Can query your knowledgebase      |

You define and enforce scopes in your API logic.

---

## 📋 Token Claims Structure (JWT Payload)

```json
{
  "sub": "agent-123",
  "scopes": ["read:reports", "send:email"],
  "iat": 1718700000,
  "exp": 1718703600
}
```

---

## 🛡️ Backend Authorization Logic

On your API server (Java, Node.js, Go, etc.), verify:

* Signature of the token
* Agent identity
* Validity (not expired or tampered)
* Allowed scopes for the resource

Example in pseudocode:

```python
if not "read:reports" in jwt_payload["scopes"]:
    return 403 Forbidden
```

---

## 🔄 Token Refresh (Coming Soon)

Tokens are currently short-lived. In future versions, refresh token support will be added with offline scopes.

---

## 🧪 Testing Auth Flow

Use `tests/test_example_usage.py` to simulate:

* Agent registration
* Token issuance
* Secure API call

You can also mock your backend using `requests_mock`.

---

## 📎 Related Docs

* [Getting Started](./getting_started.md)
* [Using with LangChain](./using_with_langchain.md)
* [Examples](./examples.md)

```
