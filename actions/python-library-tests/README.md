# Python Library Tests

Run mypy type checks and pytest with coverage for Python libraries. Includes optional Code Coverage Summary commenting on pull requests.

## Inputs

- **python-version**: Python version to set up (default: `3.x`).
- **working-directory**: Directory to run installs and tests from (default: `.`).
- **install-editable**: Install the package in editable mode via `pip install -e .` if `setup.py` or `pyproject.toml` exists (default: `true`).
- **mypy**: Run mypy type checks (default: `true`).
- **mypy-targets**: Space-separated paths/modules to pass to mypy when no config file is detected (default: `.`).
- **mypy-args**: Extra args passed to mypy (default: empty).
- **pytest-args**: Extra args passed to pytest (default: empty).

### Optional Coverage Report

- **coverage-report**: Generate a Code Coverage Summary and post a sticky PR comment (default: `false`).
- **coverage-file**: Path/glob to coverage XML (default: `coverage.xml`). Resolved relative to `working-directory`.
- **coverage-minimum**: Minimum coverage percentage (default: `80`).
- **coverage-fail-below-threshold**: Fail job if below minimum (default: `true`).
- **coverage-show-branch**: Show Branch Rate metrics (maps to `hide_branch_rate: false`).
- **coverage-report-name**: Unique name for the report/comment (default: empty).
- **coverage-pull-request-number**: Use when workflow trigger isn’t `pull_request` (default: empty).
- **coverage-continue-on-error**: Continue on reporting errors (default: `true`).
- **coverage-github-token**: GitHub token used for commenting; when omitted, the sticky comment action uses its own default token.

## What it does

- Sets up Python with pip caching against `requirements*.txt`, `setup.py`, and `pyproject.toml`.
- Installs from `requirements.txt` and optional dev files if present.
- Installs `pytest`, `pytest-cov`, `mypy`, and `coverage`.
- Optionally installs your package in editable mode when `setup.py` or `pyproject.toml` exists.
- Runs mypy (auto-detects config in `mypy.ini`, `setup.cfg`, or `pyproject.toml`; otherwise uses `mypy-targets`).
- Runs tests via `coverage run -m pytest` and generates `coverage.xml`.
- Optionally generates a Code Coverage Summary and posts a sticky PR comment using the `cobertura-report` composite action (wrapper for pinned third‑party actions) when `coverage-report: 'true'`.

## Examples

### Matrix across Python versions

```yaml
jobs:
  tests:
    runs-on: ubuntu-22.04
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.10", "3.11", "3.12", "3.13"]
    steps:
      - uses: actions/checkout@v5

      - name: Python Library Tests
        uses: OWNER/REPO/actions/python-library-tests@master
        with:
          python-version: ${{ matrix.python-version }}
```

### With custom mypy target and extra pytest args

```yaml
- name: Python Library Tests
  uses: OWNER/REPO/actions/python-library-tests@master
  with:
    python-version: '3.12'
    mypy-targets: "src/my_pkg"
    mypy-args: "--strict"
    pytest-args: "-q -k 'not slow'"
```

### Post coverage comment on PRs

```yaml
- name: Python Library Tests
  uses: OWNER/REPO/actions/python-library-tests@master
  with:
    coverage-report: 'true'
    coverage-minimum: '85'
    coverage-fail-below-threshold: 'true'
```

## Notes

- This action does not run `actions/checkout`; add it in your workflow before using the action.
- If you already install dependencies elsewhere, you can still use this action; installs from `requirements*.txt` are conditional on file presence, and editable install is optional.
- To skip mypy, set `mypy: 'false'`.
- To post PR comments, ensure the job has `permissions: pull-requests: write`.
- This action uses a sticky PR comment with `only_update: true`, so it updates an existing comment and does not create a new one if none exists.
