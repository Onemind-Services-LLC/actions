# Python Setup & Install

Set up Python, optionally upgrade `pip`, and install dependencies from `requirements.txt` and `requirements-dev.txt`/`requirements_dev.txt` when present. Supports extra install commands and an optional GitHub token for private dependencies.

## Inputs

- **python-version**: Python version to use (default: `3.x`).
- **working-directory**: Directory to run installs from (default: `.`).
- **github-token**: Optional token for private GitHub dependencies. Configures a temporary git URL rewrite to authenticate `https://github.com/` fetches as `https://x-access-token:<token>@github.com/` and cleans it up at the end.
- **upgrade-pip**: Upgrade pip before installs (default: `false`).
- **extra-install-commands**: Extra commands to execute for installing system or Python deps (e.g., `sudo apt-get install -y libpq-dev`).

## Behavior

- Uses `actions/setup-python@v5` to install the requested Python version.
- If provided, configures a temporary git URL rewrite using the token for private repo access and cleans it up afterward.
- Installs from the following files if they exist in the repo root:
  - `requirements.txt`
  - `requirements-dev.txt`
  - `requirements_dev.txt`
- Optionally upgrades `pip` when `upgrade-pip: true`.
- Runs any additional install commands you provide.

## Examples

### Basic Usage

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Python Setup & Install
        uses: OWNER/REPO/actions/python-setup-install@v1
        with:
          python-version: '3.12'
          upgrade-pip: 'true'
          working-directory: '.'
```

### With Private GitHub Dependencies and Extra Commands

```yaml
- name: Python Setup & Install
  uses: OWNER/REPO/actions/python-setup-install@v1
  with:
    python-version: '3.11'
    github-token: ${{ secrets.GITHUB_TOKEN }}
    upgrade-pip: 'true'
    working-directory: backend
    extra-install-commands: |
      sudo apt-get update
      sudo apt-get install -y libpq-dev
      pip install wheel
```

### Matrix of Python Versions

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    steps:
      - uses: actions/checkout@v4

      - name: Python Setup & Install
        uses: OWNER/REPO/actions/python-setup-install@v1
        with:
          python-version: ${{ matrix.python-version }}
          upgrade-pip: 'false'
```

## Notes

- For private repos referenced in `requirements.txt` (e.g., `git+https://github.com/org/repo@ref`), pass a token via `github-token`. Prefer `secrets.GITHUB_TOKEN` or a PAT with the minimal scopes required.
- Use `extra-install-commands` for OS packages or custom pip installs. On hosted Ubuntu runners, prefix with `sudo` as needed.
- This action targets Linux/macOS shells (`bash`).
