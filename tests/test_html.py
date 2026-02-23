from __future__ import annotations

from pathlib import Path

from sphinx.testing.util import SphinxTestApp


def test_hexdump_renders_in_html() -> None:
    root = Path(__file__).parent / "roots" / "test-basic"
    app = SphinxTestApp(srcdir=root, buildername="html", freshenv=True)
    try:
        app.build()
        html = (Path(app.outdir) / "index.html").read_text(encoding="utf-8")
    finally:
        app.cleanup()

    expected = "00000000  48 65 6C 6C 6F 2C 20 68  65 78 64 75 6D 70 21 0A  Hello, hexdump!."
    assert "00000000" in html
    assert expected in html
