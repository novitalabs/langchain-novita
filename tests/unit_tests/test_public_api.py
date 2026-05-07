"""Test the public package API."""

import langchain_novita


def test_top_level_exports_only_supported_public_api() -> None:
    assert langchain_novita.__all__ == ["NovitaSandbox", "__version__"]


def test_novita_sandbox_is_top_level_export() -> None:
    from langchain_novita import NovitaSandbox

    assert NovitaSandbox.__name__ == "NovitaSandbox"
