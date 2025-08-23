# Python Library Tests

Run mypy type checks and pytest with coverage for Python libraries. Includes optional Cobertura coverage commenting on pull requests.

## Inputs

- **python-version**: Python version to set up (default: `3.x`).
- **working-directory**: Directory to run installs and tests from (default: `.`).
- **install-editable**: Install the package in editable mode via `pip install -e .` if `setup.py` or `pyproject.toml` exists (default: `true`).
- **mypy**: Run mypy type checks (default: `true`).
- **mypy-targets**: Space-separated paths/modules to pass to mypy when no config file is detected (default: `.`).
- **mypy-args**: Extra args passed to mypy (default: empty).
- **pytest-args**: Extra args passed to pytest (default: empty).

### Optional Coverage Report

- **coverage-report**: Enable Cobertura coverage comment (default: `false`).
- **coverage-file**: Path/glob to coverage XML (default: `coverage.xml`).
- **coverage-reporter-token**: Token for reporter (required by this action). Pass a repo-scoped token such as `${{ secrets.GIT_TOKEN }}`.
- **coverage-skip-covered**: Skip files with 100% coverage (default: `true`).
- **coverage-minimum**: Minimum coverage percentage (default: `80`).
- **coverage-fail-below-threshold**: Fail job if below minimum (default: `true`).
- **coverage-show-line**: Show line coverage column (default: `true`).
- **coverage-show-branch**: Show branch coverage column (default: `true`).
- **coverage-show-class-names**: Show class names instead of file names (default: `false`).
- **coverage-show-missing**: Show missing lines per module (default: `true`).
- **coverage-only-changed-files**: Only show coverage for changed files (default: `false`).
- **coverage-report-name**: Unique name for the report/comment (default: empty).
- **coverage-pull-request-number**: Use when workflow trigger isn’t `pull_request` (default: empty).
- **coverage-continue-on-error**: Continue on reporting errors (default: `true`).

## What it does

- Sets up Python with pip caching against `requirements*.txt`, `setup.py`, and `pyproject.toml`.
- Installs from `requirements.txt` and optional dev files if present.
- Installs `pytest`, `pytest-cov`, `mypy`, and `coverage`.
- Optionally installs your package in editable mode when `setup.py` or `pyproject.toml` exists.
- Runs mypy (auto-detects config in `mypy.ini`, `setup.cfg`, or `pyproject.toml`; otherwise uses `mypy-targets`).
- Runs tests via `coverage run -m pytest` and generates `coverage.xml`.
- Optionally posts a Cobertura report comment using a pinned action when `coverage-report: 'true'`.

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
    coverage-reporter-token: ${{ secrets.GIT_TOKEN }}
    coverage-minimum: '85'
    coverage-fail-below-threshold: 'true'
```

## Notes

- This action does not run `actions/checkout`; add it in your workflow before using the action.
- If you already install dependencies elsewhere, you can still use this action; installs from `requirements*.txt` are conditional on file presence, and editable install is optional.
- To skip mypy, set `mypy: 'false'`.

