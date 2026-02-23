"""Directive implementation for rendering classic hexdumps."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective


def _is_ascii_printable(value: int) -> bool:
    return 0x20 <= value <= 0x7E


def _ascii_column(data: bytes) -> str:
    return "".join(chr(byte) if _is_ascii_printable(byte) else "." for byte in data)


def _hex_column(data: bytes, bytes_per_line: int, uppercase: bool) -> str:
    """Format the hex section, including deterministic spacing and padding."""
    fmt = "{:02X}" if uppercase else "{:02x}"
    cells = [fmt.format(data[idx]) if idx < len(data) else "  " for idx in range(bytes_per_line)]

    midpoint = bytes_per_line // 2
    if 0 < midpoint < bytes_per_line:
        left = " ".join(cells[:midpoint])
        right = " ".join(cells[midpoint:])
        return f"{left}  {right}"

    return " ".join(cells)


def format_hexdump_line(offset: int, data: bytes, bytes_per_line: int, uppercase: bool = True) -> str:
    """Render one classic hexdump line with aligned ASCII column."""
    hex_part = _hex_column(data, bytes_per_line=bytes_per_line, uppercase=uppercase)
    ascii_part = _ascii_column(data)
    return f"{offset:08X}  {hex_part}  {ascii_part}"


def _read_lines(
    path: Path,
    *,
    start: int,
    length: int,
    max_lines: int,
    bytes_per_line: int,
    uppercase: bool,
) -> Iterable[str]:
    """Stream hexdump lines from ``path`` with optional bounds."""
    read_limit: int | None = None
    if length > 0:
        read_limit = length
    if max_lines > 0:
        max_line_bytes = max_lines * bytes_per_line
        read_limit = max_line_bytes if read_limit is None else min(read_limit, max_line_bytes)

    current_offset = start
    remaining = read_limit
    emitted = 0

    with path.open("rb") as handle:
        handle.seek(start)

        while True:
            if max_lines > 0 and emitted >= max_lines:
                break
            if remaining is not None and remaining <= 0:
                break

            chunk_size = bytes_per_line if remaining is None else min(bytes_per_line, remaining)
            chunk = handle.read(chunk_size)
            if not chunk:
                break

            yield format_hexdump_line(
                offset=current_offset,
                data=chunk,
                bytes_per_line=bytes_per_line,
                uppercase=uppercase,
            )
            emitted += 1
            current_offset += len(chunk)
            if remaining is not None:
                remaining -= len(chunk)


class HexdumpDirective(SphinxDirective):
    """Render a file as a classic, monospaced hexdump literal block."""

    required_arguments = 1
    optional_arguments = 0
    has_content = False

    option_spec = {
        "bytes-per-line": directives.positive_int,
        "lowercase": directives.flag,
        "uppercase": directives.flag,
        "start": directives.nonnegative_int,
        "length": directives.nonnegative_int,
        "max-lines": directives.nonnegative_int,
    }

    def run(self) -> list[nodes.Node]:
        env = self.env
        raw_path = self.arguments[0]
        source_root = Path(env.srcdir)

        candidate = Path(raw_path)
        if candidate.is_absolute():
            resolved = candidate.expanduser().resolve()
        else:
            resolved = (source_root / candidate).resolve()

        if not resolved.exists() or not resolved.is_file():
            msg = (
                f'hexdump target file not found: argument="{raw_path}", '
                f'resolved="{resolved}"'
            )
            return [self.state_machine.reporter.error(msg, line=self.lineno)]

        env.note_dependency(str(resolved))

        bytes_per_line = self.options.get("bytes-per-line", 16)
        start = self.options.get("start", 0)
        length = self.options.get("length", 0)
        max_lines = self.options.get("max-lines", 0)

        use_uppercase = "lowercase" not in self.options
        if "uppercase" in self.options:
            use_uppercase = True

        lines = _read_lines(
            resolved,
            start=start,
            length=length,
            max_lines=max_lines,
            bytes_per_line=bytes_per_line,
            uppercase=use_uppercase,
        )
        text = "\n".join(lines)

        block = nodes.literal_block(text, text)
        block["language"] = "text"
        return [block]
