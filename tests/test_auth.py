import pytest
import base64
import json

from spokeagent_sdk.auth import AgentToken


def encode_jwt_payload(payload: dict) -> str:
    """
    Helper function to base64-url encode a JWT payload.
    """
    json_bytes = json.dumps(payload).encode("utf-8")
    b64_bytes = base64.urlsafe_b64encode(json_bytes)
    return b64_bytes.decode("utf-8").rstrip("=")


def generate_jwt(payload: dict) -> str:
    """
    Creates a fake JWT with a given payload.
    (Header and signature are dummies; this is for non-validating tests.)
    """
    header = encode_jwt_payload({"alg": "HS256", "typ": "JWT"})
    body = encode_jwt_payload(payload)
    return f"{header}.{body}.signature"


def test_decode_jwt_payload():
    payload = {"agent": "langchain-bot", "scope": "read:reports", "exp": 9999999999}
    fake_jwt = generate_jwt(payload)

    token = AgentToken(fake_jwt)
    decoded = token.decode_jwt_payload()

    assert decoded["agent"] == "langchain-bot"
    assert decoded["scope"] == "read:reports"
    assert decoded["exp"] == 9999999999


def test_get_scope_string():
    payload = {"scope": "read:logs write:alerts"}
    fake_jwt = generate_jwt(payload)

    token = AgentToken(fake_jwt)
    scopes = token.get_scope()

    assert scopes == ["read:logs", "write:alerts"]


def test_get_scope_list():
    payload = {"scope": ["read:secrets", "send:alerts"]}
    fake_jwt = generate_jwt(payload)

    token = AgentToken(fake_jwt)
    scopes = token.get_scope()

    assert scopes == ["read:secrets", "send:alerts"]


def test_get_expiry():
    payload = {"exp": 1890000000}
    fake_jwt = generate_jwt(payload)

    token = AgentToken(fake_jwt)
    expiry = token.get_expiry()

    assert expiry == 1890000000


def test_invalid_jwt_format():
    token = AgentToken("not.a.valid.token")
    assert token.decode_jwt_payload() is None
