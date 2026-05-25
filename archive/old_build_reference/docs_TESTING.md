Testing
=======

Quick start:

Install dev dependencies and run tests:

```bash
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
python run_tests.py
```

CI: GitHub Actions workflow at `.github/workflows/pytest.yml` runs tests on push/PR.

Pre-commit: install pre-commit and run `pre-commit install` to enable the local pytest hook.

Autosave-and-test helper
------------------------

A small helper `save_and_test.py` will create a temporary `WIP` commit, run the test
suite, and automatically undo the WIP commit if tests fail so your working tree
remains unchanged.

Usage:

```bash
python save_and_test.py
```

Notes:
- If tests pass the WIP commit remains as a local checkpoint you can `git commit --amend`
	or squash later during cleanup.
- If tests fail the script resets the WIP commit but leaves your changes in the working tree.

