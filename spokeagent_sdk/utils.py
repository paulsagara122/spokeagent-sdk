# Helper functions (optional)
import base64
import json
from typing import Optional


def decode_jwt_segment(segment: str) -> Optional[dict]:
    """
    Decodes a base64-encoded JWT segment (typically the payload).

    Args:
        segment (str): Base64URL-encoded JWT segment.

    Returns:
        dict or None: Decoded JSON payload if valid, else None.
    """
    try:
        padding = '=' * (4 - len(segment) % 4) if len(segment) % 4 != 0 else ''
        segment += padding
        decoded = base64.urlsafe_b64decode(segment.encode("utf-8"))
        return json.loads(decoded)
    except Exception:
        return None


def safe_get(data: dict, path: str, default=None):
    """
    Safely retrieves nested properties from a dictionary using dot notation.

    Example:
        user = {"meta": {"profile": {"name": "Alice"}}}
        safe_get(user, "meta.profile.name")  # "Alice"

    Args:
        data (dict): The dictionary to traverse.
        path (str): Dot-separated path string.
        default: Default value if any part of the path is missing.

    Returns:
        The value at the nested path, or default if not found.
    """
    try:
        keys = path.split(".")
        for key in keys:
            data = data[key]
        return data
    except (KeyError, TypeError):
        return default


def redact_token(token: str, visible_chars: int = 6) -> str:
    """
    Returns a redacted version of a token for logging.

    Args:
        token (str): The full token string.
        visible_chars (int): Number of characters to show at the end.

    Returns:
        str: Redacted token (e.g., '****c9d98f').
    """
    if not token or len(token) <= visible_chars:
        return "****"
    return f"****{token[-visible_chars:]}"
