"""
spokeagent_sdk
==============

Python SDK for SpokeAgent – IAM for Autonomous AI Agents.

Usage:

    from spokeagent_sdk import SpokeAgentClient, SpokeAgentConfig

    config = SpokeAgentConfig(base_url="https://api.spokeagent.com", api_key="your_api_key")
    client = SpokeAgentClient(config)

    agent = client.register_agent("my-agent", metadata={"purpose": "data-analysis"})
    token = client.get_token(agent_id=agent["id"], scopes=["read:data", "write:logs"])
    response = client.call_api("/secure/data", method="GET")
"""

from .client import SpokeAgentClient
from .auth import AgentToken
from .config import SpokeAgentConfig
from .errors import SpokeAgentError

__all__ = [
    "SpokeAgentClient",
    "SpokeAgentConfig",
    "AgentToken",
    "SpokeAgentError"
]
