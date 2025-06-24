import pytest
import requests_mock
from spokeagent_sdk import SpokeAgentClient, SpokeAgentConfig


@pytest.fixture
def mock_config():
    return SpokeAgentConfig(base_url="http://localhost:8000", api_key="fake-api-key")


def test_register_agent(mock_config):
    client = SpokeAgentClient(mock_config)
    with requests_mock.Mocker() as m:
        m.post("http://localhost:8000/api/agents/register", json={"id": "agent123", "name": "testbot"})

        agent = client.register_agent("testbot")
        assert agent["id"] == "agent123"
        assert agent["name"] == "testbot"


def test_get_token(mock_config):
    client = SpokeAgentClient(mock_config)
    with requests_mock.Mocker() as m:
        m.post("http://localhost:8000/api/agents/token", json={"token": "abc123"})

        token = client.get_token("agent123", scopes=["read:data"])
        assert token == "abc123"


def test_call_api(mock_config):
    client = SpokeAgentClient(mock_config)
    client.token = "abc123"  # Simulate token already fetched

    with requests_mock.Mocker() as m:
        m.get("http://localhost:8000/secure/data", json={"result": "success"})

        response = client.call_api("/secure/data", method="GET")
        assert response["result"] == "success"
