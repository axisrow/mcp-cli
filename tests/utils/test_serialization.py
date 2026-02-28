# tests/utils/test_serialization.py
"""Tests for unwrap_tool_result in mcp_cli.utils.serialization."""

from __future__ import annotations

import pytest

from mcp_cli.utils.serialization import unwrap_tool_result


class TestUnwrapToolResult:
    """Tests for the MCP dict unwrapping path."""

    def test_success_returns_content(self):
        result = unwrap_tool_result({"isError": False, "content": "hello"})
        assert result == "hello"

    def test_error_raises_with_content_fallback(self):
        with pytest.raises(RuntimeError, match="boom"):
            unwrap_tool_result({"isError": True, "content": "boom"})

    def test_error_prefers_error_field_over_content(self):
        with pytest.raises(RuntimeError, match="specific error"):
            unwrap_tool_result(
                {"isError": True, "error": "specific error", "content": "fallback"}
            )

    def test_error_without_content_uses_default_message(self):
        with pytest.raises(RuntimeError, match="Tool returned an error"):
            unwrap_tool_result({"isError": True, "content": ""})

    def test_passthrough_plain_values(self):
        assert unwrap_tool_result("plain") == "plain"
        assert unwrap_tool_result(42) == 42
        assert unwrap_tool_result(None) is None

    def test_passthrough_dict_without_iserror(self):
        d = {"foo": "bar"}
        assert unwrap_tool_result(d) == {"foo": "bar"}
