from __future__ import annotations

from pathlib import Path

from sphinx.testing.util import SphinxTestApp


def test_hexdump_renders_in_latex() -> None:
    root = Path(__file__).parent / "roots" / "test-basic"
    app = SphinxTestApp(srcdir=root, buildername="latex", freshenv=True)
    try:
        app.build()
        tex_files = list(Path(app.outdir).glob("*.tex"))
        assert tex_files, "Expected LaTeX builder to emit a .tex file"
        tex = tex_files[0].read_text(encoding="utf-8")
    finally:
        app.cleanup()

    assert "00000000" in tex
    assert "48 65 6C 6C 6F 2C 20 68  65 78 64 75 6D 70 21 0A" in tex
