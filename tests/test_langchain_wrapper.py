import pytest
from unittest.mock import patch, MagicMock
from langchain.tools import Tool

from spokeagent_sdk.config import SpokeAgentConfig
from spokeagent_sdk.langchain_wrapper import SpokeAgentTool


@pytest.fixture
def mock_config():
    return SpokeAgentConfig(base_url="http://fake-url.com", api_key="fake-api-key")


@patch("spokeagent_sdk.langchain_wrapper.SpokeAgentClient")
def test_langchain_tool_creation(mock_client_class, mock_config):
    # Mock client behavior
    mock_client = MagicMock()
    mock_client.register_agent.return_value = {"id": "agent123", "name": "test-agent"}
    mock_client.get_token.return_value = "mock-token"
    mock_client.call_api.return_value = {"result": "42"}

    mock_client_class.return_value = mock_client

    # Create tool
    agent_tool = SpokeAgentTool(
        config=mock_config,
        agent_name="test-agent",
        scopes=["read:data"]
    )

    tool = agent_tool.as_tool(
        name="MockDataTool",
        description="Fetches data using SpokeAgent",
        endpoint="/api/data",
        method="POST"
    )

    # Assertions
    assert isinstance(tool, Tool)
    assert tool.name == "MockDataTool"
    assert "Fetches data" in tool.description

    result = tool.run("What is the answer?")
    assert "42" in result

    mock_client.register_agent.assert_called_once()
    mock_client.get_token.assert_called_once()
    mock_client.call_api.assert_called_once_with(
        endpoint="/api/data",
        method="POST",
        data={"query": "What is the answer?"}
    )


@patch("spokeagent_sdk.langchain_wrapper.SpokeAgentClient")
def test_input_map_functionality(mock_client_class, mock_config):
    # Mock client behavior
    mock_client = MagicMock()
    mock_client.register_agent.return_value = {"id": "agent456"}
    mock_client.get_token.return_value = "mock-token"
    mock_client.call_api.return_value = {"response": "OK"}

    mock_client_class.return_value = mock_client

    def map_input(text):
        return {"input": text.upper()}

    tool = SpokeAgentTool(
        config=mock_config,
        agent_name="uppercase-agent",
        scopes=["transform"]
    ).as_tool(
        name="UppercaseTool",
        description="Converts input to uppercase",
        endpoint="/api/uppercase",
        input_map=map_input
    )

    result = tool.run("hello world")
    assert "OK" in result

    mock_client.call_api.assert_called_once_with(
        endpoint="/api/uppercase",
        method="POST",
        data={"input": "HELLO WORLD"}
    )
