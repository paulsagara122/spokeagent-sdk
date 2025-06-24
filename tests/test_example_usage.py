import pytest
from unittest.mock import patch, MagicMock
from spokeagent_sdk import SpokeAgentClient, SpokeAgentConfig


@pytest.fixture
def mock_config():
    return SpokeAgentConfig(
        base_url="https://api.spokeagent.com",
        api_key="test-api-key"
    )


@patch("spokeagent_sdk.client.requests.post")
@patch("spokeagent_sdk.client.requests.get")  # ✅ Correctly mocking the GET request
def test_full_agent_flow(mock_get, mock_post, mock_config):
    # 1. Mock /api/agents/register response
    register_response = MagicMock()
    register_response.status_code = 200
    register_response.json.return_value = {
        "id": "agent-001",
        "name": "langchain-reporter-bot"
    }

    # 2. Mock /api/agents/token response
    token_response = MagicMock()
    token_response.status_code = 200
    token_response.json.return_value = {
        "token": "fake-jwt-token"
    }

    # Set side effect: first POST = register, second POST = token
    mock_post.side_effect = [register_response, token_response]

    # 3. Mock GET /api/reports/today response
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "report": "This is the summary for today"
    }

    # 4. Execute the full SDK flow
    client = SpokeAgentClient(mock_config)

    agent = client.register_agent("langchain-reporter-bot", metadata={"purpose": "demo"})
    assert agent["id"] == "agent-001"

    token = client.get_token(agent_id=agent["id"], scopes=["read:reports"])
    assert token == "fake-jwt-token"

    result = client.call_api(endpoint="/api/reports/today", method="GET")
    assert result["report"] == "This is the summary for today"

    # 5. Assert internal behavior
    assert mock_post.call_count == 2

    mock_get.assert_called_once_with(
        "https://api.spokeagent.com/api/reports/today",  # ✅ url passed as positional arg
        headers={
            "Authorization": "Bearer fake-jwt-token",
            "Content-Type": "application/json"
        }
    )
