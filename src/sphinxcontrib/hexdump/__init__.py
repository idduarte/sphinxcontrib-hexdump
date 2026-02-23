"""Sphinx extension entry point for sphinxcontrib-hexdump."""

from __future__ import annotations

from sphinx.application import Sphinx

from .directive import HexdumpDirective

__all__ = ["setup"]


def setup(app: Sphinx) -> dict[str, object]:
    """Register the ``hexdump`` directive with Sphinx."""
    app.add_directive("hexdump", HexdumpDirective)
    return {
        "version": "0.1.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

