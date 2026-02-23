# Publishing

This project supports two release flows:

- Test release to TestPyPI with tag `test-vX.Y.Z`
- Production release to PyPI with tag `vX.Y.Z`

## One-time setup (Trusted Publishing)

### 1) Configure PyPI publisher

In PyPI project settings, add a trusted publisher:

- Owner: `idduarte`
- Repository: `sphinxcontrib-hexdump`
- Workflow: `publish.yml`

### 2) Configure TestPyPI publisher

In TestPyPI project settings, add a trusted publisher:

- Owner: `idduarte`
- Repository: `sphinxcontrib-hexdump`
- Workflow: `publish-testpypi.yml`

## Local validation before tagging

```bash
python -m pip install --upgrade pip
pip install -e .[test]
python -m pytest
python -m sphinx -b html docs docs/_build/html
python -m sphinx -b latex docs docs/_build/latex
python -m build
python -m twine check dist/*
```

## Test release flow (TestPyPI)

1. Bump version in `pyproject.toml` (for example `0.1.1`).
2. Commit and push:
   ```bash
   git add pyproject.toml
   git commit -m "Bump version to 0.1.1"
   git push origin main
   ```
3. Create and push test tag:
   ```bash
   git tag test-v0.1.1
   git push origin test-v0.1.1
   ```
4. Verify workflow `Publish TestPyPI` in GitHub Actions.
5. Validate install from TestPyPI:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple sphinxcontrib-hexdump==0.1.1
   ```

## Production release flow (PyPI)

1. Ensure target version in `pyproject.toml` is final.
2. Tag and push:
   ```bash
   git tag v0.1.1
   git push origin v0.1.1
   ```
3. Verify workflow `Publish` in GitHub Actions.
4. Validate from PyPI:
   ```bash
   pip install -U sphinxcontrib-hexdump==0.1.1
   ```

## Optional manual upload (fallback)

```bash
python -m build
python -m twine check dist/*
python -m twine upload dist/*
```
