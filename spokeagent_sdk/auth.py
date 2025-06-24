# Token management (AgentToken)
import base64
import json
from typing import Optional


class AgentToken:
    """
    Wrapper class for agent tokens (e.g., JWTs or opaque tokens).
    Includes helper methods for decoding and inspection.
    """

    def __init__(self, token: str):
        self.token = token.strip()

    def __str__(self):
        return self.token

    def get_raw(self) -> str:
        """Return the raw token string."""
        return self.token

    def decode_jwt_payload(self) -> Optional[dict]:
        """
        Decodes the payload part of a JWT token (non-validated).

        Returns:
            dict or None: Decoded payload or None if not a JWT.
        """
        try:
            parts = self.token.split(".")
            if len(parts) != 3:
                return None
            payload_encoded = parts[1]
            # Pad the base64 string if required
            padding = '=' * (4 - len(payload_encoded) % 4)
            payload_encoded += padding
            decoded_bytes = base64.urlsafe_b64decode(payload_encoded.encode("utf-8"))
            return json.loads(decoded_bytes)
        except Exception:
            return None

    def get_scope(self) -> Optional[list]:
        """
        Attempts to extract scopes from JWT payload.

        Returns:
            list or None: List of scopes or None if not found.
        """
        payload = self.decode_jwt_payload()
        if payload and "scope" in payload:
            if isinstance(payload["scope"], str):
                return payload["scope"].split(" ")
            elif isinstance(payload["scope"], list):
                return payload["scope"]
        return None

    def get_expiry(self) -> Optional[int]:
        """
        Returns expiry timestamp (Unix) from the JWT if available.

        Returns:
            int or None
        """
        payload = self.decode_jwt_payload()
        return payload.get("exp") if payload else None
