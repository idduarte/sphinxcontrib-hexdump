# sphinxcontrib-hexdump

`sphinxcontrib-hexdump` is a Sphinx extension that renders files as classic monochrome hexdumps using a reStructuredText directive.

## Features

- Reads any file type as raw binary bytes.
- Produces deterministic output with pure Python formatting.
- Emits a single literal code block that works consistently in HTML and LaTeX builders.
- Supports offset/length/line limiting for large files.

## Installation

```bash
pip install sphinxcontrib-hexdump
```

For local development:

```bash
pip install -e .[test]
```

## Enable the extension

Add to `conf.py`:

```python
extensions = [
    "sphinxcontrib.hexdump",
]
```

## Directive usage

```rst
.. hexdump:: ../artifacts/firmware.elf
   :bytes-per-line: 16
   :start: 0
   :length: 256
   :max-lines: 64
```

Lowercase bytes are optional:

```rst
.. hexdump:: ../artifacts/firmware.elf
   :lowercase:
```

## Options

- `:bytes-per-line:` integer >= 1, default `16`
- `:lowercase:` flag; if present, byte hex values are lowercase (default is uppercase)
- `:start:` integer >= 0, default `0`
- `:length:` integer >= 0, default `0` (read until EOF)
- `:max-lines:` integer >= 0, default `0` (no line limit)

## Notes

- Paths are resolved relative to the Sphinx source directory (`env.srcdir`).
- Files outside the docs directory are allowed if they exist.
- For very large files, prefer `:length:` and/or `:max-lines:` to keep output size bounded.

## Compatibility

- Python 3.10+
- Sphinx 6.2+

## License

MIT
