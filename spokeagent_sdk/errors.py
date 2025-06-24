# Custom exceptions for clarity
class SpokeAgentError(Exception):
    """
    Base exception for all SpokeAgent SDK errors.
    """
    def __init__(self, message: str):
        super().__init__(message)


class AgentRegistrationError(SpokeAgentError):
    """
    Raised when agent registration fails.
    """
    def __init__(self, message: str = "Failed to register agent."):
        super().__init__(message)


class TokenRequestError(SpokeAgentError):
    """
    Raised when token request or parsing fails.
    """
    def __init__(self, message: str = "Failed to retrieve or parse token."):
        super().__init__(message)


class APIRequestError(SpokeAgentError):
    """
    Raised for general API call failures.
    """
    def __init__(self, message: str = "API call failed."):
        super().__init__(message)
