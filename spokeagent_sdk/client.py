# Core client class: register_agent, get_token, call_api
import requests
from typing import List, Optional, Dict

from .config import SpokeAgentConfig
from .errors import (
    SpokeAgentError,
    AgentRegistrationError,
    TokenRequestError,
    APIRequestError
)


class SpokeAgentClient:
    def __init__(self, config: SpokeAgentConfig):
        """
        Initialize the SpokeAgent client.

        Args:
            config (SpokeAgentConfig): Configuration object with base_url and API key.
        """
        self.config = config
        self.base_url = config.base_url.rstrip("/")
        self.api_key = config.api_key
        self.token: Optional[str] = None

    def register_agent(self, agent_name: str, metadata: Optional[Dict] = None) -> Dict:
        """
        Registers an AI agent and returns its identity.

        Args:
            agent_name (str): Name of the agent.
            metadata (dict): Optional metadata describing the agent.

        Returns:
            dict: Agent details from the API.

        Raises:
            AgentRegistrationError: If registration fails.
        """
        url = f"{self.base_url}/api/agents/register"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "name": agent_name,
            "metadata": metadata or {}
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise AgentRegistrationError(f"Agent registration failed: {str(e)}") from e

    def get_token(self, agent_id: str, scopes: List[str]) -> str:
        """
        Retrieves a scoped token for the agent.

        Args:
            agent_id (str): Registered agent ID.
            scopes (list of str): List of permission scopes.

        Returns:
            str: JWT or token string.

        Raises:
            TokenRequestError: If token cannot be fetched.
        """
        url = f"{self.base_url}/api/agents/token"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "agent_id": agent_id,
            "scopes": scopes
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            self.token = response.json().get("token")
            if not self.token:
                raise TokenRequestError("Token not found in response.")
            return self.token
        except requests.RequestException as e:
            raise TokenRequestError(f"Failed to fetch token: {str(e)}") from e

    def call_api(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Dict:
        """
        Makes an authenticated API call on behalf of the agent.

        Args:
            endpoint (str): API endpoint path (e.g., /secure/data).
            method (str): HTTP method ('GET', 'POST').
            data (dict): Optional request body.

        Returns:
            dict: API response.

        Raises:
            APIRequestError: If request fails.
        """
        if not self.token:
            raise APIRequestError("Token not available. Call get_token() first.")

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        url = f"{self.base_url}{endpoint}"

        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, json=data or {}, headers=headers)
            else:
                raise APIRequestError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIRequestError(f"API call failed: {str(e)}") from e
