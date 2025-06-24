### 📄 `docs/faq.md`

````markdown
# ❓ Frequently Asked Questions (FAQ)

This page addresses common questions about the **SpokeAgent SDK**, agent registration, authentication, and integration with LangChain.

---

## 💡 General

### 🔹 What is SpokeAgent?

SpokeAgent is an identity and access management layer designed specifically for **autonomous AI agents** (e.g., LangChain, AutoGen, custom bots). It allows secure registration, scoped authentication, and API access control for machine agents.

---

## 🛠️ Installation & Setup

### 🔹 How do I install the SDK?

Use pip with the provided requirements:

```bash
pip install -r requirements.txt
````

For development/testing:

```bash
pip install -r requirements-dev.txt
```

---

### 🔹 Do I need an API key?

Yes. You must use an **admin API key** to register agents and issue scoped tokens. Contact your AuthSpoke admin portal to obtain one.

---

## 👤 Agents & Authentication

### 🔹 What is an AI agent in this context?

An agent is a program, script, or bot that requires a unique identity and scoped access to backend APIs — similar to a "service account" for machines.

---

### 🔹 What are scopes?

Scopes define what an agent is allowed to do. For example:

* `read:reports`
* `write:summary`
* `send:email`

Only APIs matching those scopes can be called with the token.

---

### 🔹 How long do tokens last?

Tokens are short-lived for security. You’ll need to request a new token using your admin key when they expire (default TTL configurable on the server).

---

## 🔐 API Access

### 🔹 How do I call a secure API?

Use `client.call_api(...)` with the registered agent and token. The SDK will inject the JWT token in the Authorization header automatically.

---

### 🔹 Can I restrict access to specific endpoints?

Yes — your backend should enforce **scope checks** against the JWT token claims.

---

## 🤖 LangChain Integration

### 🔹 How do I use SpokeAgent with LangChain?

You can wrap any internal API as a LangChain Tool using the `SpokeAgentTool`:

```python
from spokeagent_sdk.langchain_wrapper import SpokeAgentTool
```

See: [docs/using\_with\_langchain.md](./using_with_langchain.md)

---

### 🔹 Can I define custom input mappings?

Yes — use the `input_map` parameter when defining the tool to convert prompts into payloads.

---

## 🧪 Testing & Dev

### 🔹 How do I mock agent registration or API calls?

Use `unittest.mock.patch` to override network calls in tests. We provide full examples in `tests/`.

---

### 🔹 Is there a sandbox or mock mode?

Coming soon — currently, you should mock API responses using `requests_mock` or `MagicMock`.

---

## 📦 Miscellaneous

### 🔹 Is this open source?

No. This SDK is proprietary to **AuthnIdentity Inc.**, licensed only to authorized users.

---

### 🔹 How is this different from traditional IAM?

SpokeAgent is AI-first, built for **agent identity**, **scoped tokens**, and **LangChain-compatible workflows**. It’s IAM reimagined for the autonomous AI era.

---

## 📩 Still Have Questions?

Feel free to reach out to your **AuthSpoke support contact** or email:
📧 `sagar.paul@authspoke.com`

---
