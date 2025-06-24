# Optional LangChain adapter
from langchain.tools import Tool
from typing import List, Optional, Callable

from spokeagent_sdk import SpokeAgentClient, SpokeAgentConfig


class SpokeAgentTool:
    """
    Wraps a secure SpokeAgent endpoint as a LangChain Tool.
    """

    def __init__(
        self,
        config: SpokeAgentConfig,
        agent_name: str,
        scopes: List[str],
        metadata: Optional[dict] = None
    ):
        """
        Initialize a new SpokeAgentTool instance.

        Args:
            config (SpokeAgentConfig): Configuration with base_url and API key.
            agent_name (str): Name of the AI agent to register.
            scopes (list): Scopes for token access (e.g., ['read:logs']).
            metadata (dict): Optional metadata about the agent.
        """
        self.client = SpokeAgentClient(config)
        self.agent = self.client.register_agent(agent_name, metadata)
        self.client.get_token(self.agent["id"], scopes)

    def as_tool(
        self,
        name: str,
        description: str,
        endpoint: str,
        method: str = "POST",
        input_map: Optional[Callable[[str], dict]] = None
    ) -> Tool:
        """
        Returns a LangChain-compatible Tool for this agent's secure API access.

        Args:
            name (str): Tool name for LangChain agent.
            description (str): Natural language description.
            endpoint (str): API endpoint (e.g., /api/query/knowledge).
            method (str): HTTP method (default is POST).
            input_map (Callable): Optional function to transform user input to API input.

        Returns:
            Tool: LangChain Tool instance.
        """
        def _fn(input_text: str) -> str:
            payload = input_map(input_text) if input_map else {"query": input_text}
            result = self.client.call_api(endpoint=endpoint, method=method, data=payload)
            return str(result)

        return Tool(name=name, func=_fn, description=description)
