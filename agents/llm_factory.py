"""
Deterministic local mock response engine; no external model providers implemented.
"""
from typing import Dict, Any, Optional
from .base import PHIGuard


class MockLLM:
    def __init__(self, system_name: str = "Sphincs Stateless Hash Sign"):
        self.system_name = system_name

    def invoke(self, prompt: str) -> str:
        PHIGuard.assert_no_phi(prompt)
        return (
            f"[{self.system_name} local demo]: This is a deterministic text response, "
            "not a cryptographic or standards-conformance verification. "
            f"Received inquiry: {prompt[:60]!r}."
        )


class LLMFactory:
    """Creates configured LLM client instances with zero-PHI protection."""

    @staticmethod
    def create(provider: str = "mock", system_name: str = "Sphincs Stateless Hash Sign"):
        prov = str(provider).lower()
        if prov in ["mock", "deterministic", "test"]:
            return MockLLM(system_name)
        raise ValueError(
            f"Unsupported provider {provider!r}. Only the local deterministic 'mock' "
            "provider is implemented; no external model is called."
        )
