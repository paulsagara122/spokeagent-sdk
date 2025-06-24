import pytest
import spokeagent_sdk


def test_init_module_exposes_public_classes():
    # Ensure __all__ matches what is actually exposed
    assert hasattr(spokeagent_sdk, "SpokeAgentClient")
    assert hasattr(spokeagent_sdk, "SpokeAgentConfig")
    assert hasattr(spokeagent_sdk, "SpokeAgentError")

    # Check types (not strict type, just callable interface)
    assert callable(spokeagent_sdk.SpokeAgentClient)
    assert callable(spokeagent_sdk.SpokeAgentConfig)
    assert issubclass(spokeagent_sdk.SpokeAgentError, Exception)
