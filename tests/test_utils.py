import pytest
import base64
import json
from spokeagent_sdk.utils import decode_jwt_segment, safe_get, redact_token


def test_decode_jwt_segment_valid():
    payload = {"user": "alice", "role": "admin"}
    json_bytes = json.dumps(payload).encode("utf-8")
    encoded_segment = base64.urlsafe_b64encode(json_bytes).decode("utf-8").rstrip("=")

    decoded = decode_jwt_segment(encoded_segment)

    assert isinstance(decoded, dict)
    assert decoded["user"] == "alice"
    assert decoded["role"] == "admin"


def test_decode_jwt_segment_invalid():
    bad_segment = "!!not_base64!!"
    result = decode_jwt_segment(bad_segment)
    assert result is None


def test_safe_get_nested_key_exists():
    data = {"meta": {"profile": {"name": "bob"}}}
    value = safe_get(data, "meta.profile.name")
    assert value == "bob"


def test_safe_get_nested_key_missing():
    data = {"meta": {"profile": {}}}
    value = safe_get(data, "meta.profile.age", default="N/A")
    assert value == "N/A"


def test_safe_get_type_error():
    data = {"meta": None}
    value = safe_get(data, "meta.profile.name", default="unknown")
    assert value == "unknown"


def test_redact_token_default():
    token = "supersecrettoken123456"
    redacted = redact_token(token)
    assert redacted.endswith("3456")
    assert redacted.startswith("****")


def test_redact_token_short_token():
    token = "123"
    redacted = redact_token(token)
    assert redacted == "****"
