# Publishing

## Build and check distributions

```bash
python -m build
twine check dist/*
```

## Upload to PyPI

```bash
twine upload dist/*
```

## Version bump and tagging

1. Update `version` in `pyproject.toml`.
2. Commit the change:
   ```bash
   git add pyproject.toml
   git commit -m "Bump version to X.Y.Z"
   ```
3. Tag the release:
   ```bash
   git tag vX.Y.Z
   git push origin main --tags
   ```
4. If GitHub trusted publishing is configured, pushing the tag triggers publish workflow.
