# NetBox Plugin Tests (Reusable Workflow)

Spin up Redis/Postgres, install NetBox and your plugin, then run Django checks and tests with coverage.

- File: `.github/workflows/netbox-plugin-tests.yml`
- Consume via: `uses: Onemind-Services-LLC/actions/.github/workflows/netbox-plugin-tests.yml@v1`

## What It Does

- Starts Redis and Postgres services using GitHub Actions services.
- Checks out the NetBox repo at the requested version and your plugin repo.
- Sets up Python and installs dependencies for NetBox and the plugin.
- Runs Django checks, migrations, collectstatic, and tests (via composite `django-test-runner`).

## Inputs

- `plugin-name` (string, required): Plugin repo directory name (e.g., `netbox_secrets`).
- `netbox-version` (string, required): NetBox git ref (e.g., `v4.3.0`).
- `python-version` (string, optional): Python version (default: `3.12`).
- `runner` (string, optional): Runner label (default: `ubuntu-22.04-sh`).

## Required Vars/Secrets

- `vars.APP_ID`: GitHub App ID for accessing private dependencies (when needed).
- `secrets.APP_PRIVATE_KEY`: GitHub App private key (PEM) used to mint an installation token.

These are used by the internal composite action `actions/create-repo-token@v1`.

## Environment and Configuration

- NetBox runs with `DJANGO_SETTINGS_MODULE=netbox.configuration`.
- Your plugin must provide a testing configuration module accessible as
  `NETBOX_CONFIGURATION=testing_configuration.configuration`.
  - Provide `testing_configuration/configuration.py` in your plugin repo.
- PYTHONPATH is augmented to include your plugin directory.

## Database and Cache

- Redis: `6379` (default), healthchecked via `redis-cli ping`.
- Postgres: `5432` (default), credentials `netbox`/`netbox`, database `netbox`.

Ensure your testing configuration matches these defaults or override via env in your plugin tests.

## Usage Example

```yaml
permissions:
  contents: read

jobs:
  test:
    uses: Onemind-Services-LLC/actions/.github/workflows/netbox-plugin-tests.yml@v1
    with:
      plugin-name: my_netbox_plugin
      netbox-version: v4.3.0
      python-version: '3.12'
      runner: ubuntu-22.04-sh
    secrets: {}
```

## Notes

- Internally uses composite actions pinned to `@v1`:
  - `actions/create-repo-token@v1`
  - `actions/python-setup-install@v1`
  - `actions/django-test-runner@v1`
- For private dependencies referenced in `requirements*.txt`, the workflow mints a repo-scoped installation token.
- Requires Docker-backed services when running locally with `act`.

## Troubleshooting

- Missing testing configuration: Ensure `testing_configuration/configuration.py` exists and is importable.
- Dependency install errors: If your plugin needs extra system packages, add them to your plugin’s requirements or install scripts; the workflow already installs `libpq-dev` for Postgres.
- Database connectivity: Confirm your plugin’s Django settings match the service host/ports provided by the runner (`localhost:5432`, `localhost:6379`).
