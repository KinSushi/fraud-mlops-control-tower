# Screenshots and content previews

Generated from real repository validation commands in GitHub Actions.

## Validation artifacts

- [validation-preview.svg](screenshots/validation-preview.svg)
- [validation-output.html](screenshots/validation-output.html)

## What the validation preview proves

The generated validation preview covers:

```text
pip install
python -m compileall
pytest
ruff
synthetic risk data generation
package import checks
small-model training with MLflow SQLite tracking
```

These visuals contain synthetic/public portfolio information only. They do not contain real banking, insurance, health, client, employer, host or credential data.

## Future UI screenshots

Future screenshots should show:

- FastAPI `/docs`;
- MLflow experiment run overview;
- generated metrics JSON;
- threshold tuning output.
