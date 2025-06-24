# Handles API base URL, API keys
import os


class SpokeAgentConfig:
    """
    Configuration class for initializing the SpokeAgent SDK.

    Example usage:

        config = SpokeAgentConfig(
            base_url="https://api.spokeagent.com",
            api_key="your_api_key"
        )
    """

    def __init__(self, base_url: str = None, api_key: str = None):
        self.base_url = base_url or os.getenv("SPOKEAGENT_BASE_URL")
        self.api_key = api_key or os.getenv("SPOKEAGENT_API_KEY")

        if not self.base_url:
            raise ValueError("Missing base_url. Provide it directly or set SPOKEAGENT_BASE_URL env variable.")

        if not self.api_key:
            raise ValueError("Missing api_key. Provide it directly or set SPOKEAGENT_API_KEY env variable.")

    def __repr__(self):
        return f"SpokeAgentConfig(base_url='{self.base_url}', api_key='***')"
