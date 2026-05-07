from __future__ import annotations

from collections.abc import Iterator
from uuid import uuid4

import pytest
from novita_sandbox.code_interpreter import Sandbox

from langchain_novita.sandbox import NovitaSandbox


@pytest.fixture(scope="class")
def backend() -> Iterator[NovitaSandbox]:
    sdk_sandbox = Sandbox.create()
    try:
        yield NovitaSandbox(sandbox=sdk_sandbox)
    finally:
        sdk_sandbox.kill()


class TestNovitaSandboxIntegration:
    def test_execute_success(self, backend: NovitaSandbox) -> None:
        result = backend.execute("printf hello")

        assert result.exit_code == 0
        assert result.output == "hello"
        assert result.truncated is False

    def test_execute_failure_returns_exit_code(self, backend: NovitaSandbox) -> None:
        result = backend.execute("python -c 'import sys; print(\"boom\"); sys.exit(7)'")

        assert result.exit_code == 7
        assert "boom" in result.output

    def test_upload_and_download_files(self, backend: NovitaSandbox) -> None:
        path = f"/tmp/langchain-novita-{uuid4().hex}.txt"
        content = b"hello from novita sandbox"

        upload_results = backend.upload_files([(path, content)])
        download_results = backend.download_files([path])

        assert upload_results[0].error is None
        assert download_results[0].error is None
        assert download_results[0].content == content

    def test_download_missing_file_returns_error(self, backend: NovitaSandbox) -> None:
        path = f"/tmp/langchain-novita-missing-{uuid4().hex}.txt"

        results = backend.download_files([path])

        assert results[0].content is None
        assert results[0].error == "file_not_found"
