# Contributing

## Development setup

```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -e .[test]
```

## Run checks

```bash
pytest
sphinx-build -b html docs docs/_build/html
sphinx-build -b latex docs docs/_build/latex
```

## Pull requests

- Keep changes focused.
- Add or update tests for behavior changes.
- Update documentation when directive behavior changes.
