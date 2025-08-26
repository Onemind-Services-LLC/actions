# Django Test Runner

Run Django checks, apply migrations, collect static files, and execute tests with coverage reporting.

## Inputs

- **working-directory**: Directory containing `manage.py` (default: `.`).
- **django-settings-module**: Settings module to export for Django commands.
- **django-settings-module-key**: Env var name to export the settings module under (default: `DJANGO_SETTINGS_MODULE`).
- **verbosity**: Django command verbosity (default: `3`).
- **test-args**: Extra args appended to `manage.py test`.
- **coverage-args**: Extra args appended to `coverage xml`.
- **coverage-source**: Comma-separated modules/paths to measure (passed to `coverage run --source`).

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

- Installs `coverage` via pip.
- Runs `makemigrations --check --dry-run` to enforce committed migrations.
- Runs `migrate -v <verbosity>`.
- Runs `collectstatic --noinput`.
- Runs `check -v <verbosity>`.
- Runs tests via `coverage run manage.py test` and generates `coverage.xml` via `coverage xml`.
  - Tip: Use `coverage-source` to restrict measurement to your app/package (e.g., only a NetBox plugin) and exclude framework code.
- Optionally generates a Code Coverage Summary and posts a sticky PR comment using the `cobertura-report` composite action (wrapper for pinned third‑party actions) when `coverage-report: 'true'`.

## Examples

### Basic

```yaml
- name: Django Test Runner
  uses: OWNER/REPO/actions/django-test-runner@master
  with:
    django-settings-module: myproj.settings
```

### With settings module and extra test args

```yaml
- name: Django Test Runner
  uses: OWNER/REPO/actions/django-test-runner@master
  with:
    django-settings-module: myproj.settings.test
    test-args: "--pattern='test_*.py'"
```

### With coverage report

```yaml
- name: Django Test Runner
  uses: OWNER/REPO/actions/django-test-runner@master
  with:
    coverage-report: 'true'
    coverage-minimum: '80'
    coverage-fail-below-threshold: 'true'
    coverage-show-branch: 'true'
    coverage-report-name: 'Django Test Coverage'

    # Only measure your app (exclude framework/libs)
    coverage-source: my_plugin_package
```

### In a subdirectory and custom verbosity

```yaml
- name: Django Test Runner
  uses: OWNER/REPO/actions/django-test-runner@master
  with:
    working-directory: backend
    verbosity: '2'
```

### Using a custom settings env var

Some projects read an alternate env var for the Django settings module. Specify the key via `django-settings-module-key`:

```yaml
- name: Django Test Runner
  uses: OWNER/REPO/actions/django-test-runner@master
  with:
    django-settings-module: testing_configuration.configuration
    django-settings-module-key: NETBOX_CONFIGURATION
```

## Notes

- Ensure DB/cache services are available before this action.
- Set any required environment variables (e.g., DB credentials) at job or step level.
- The coverage reporter runs whenever `coverage-report: 'true'`. If you want it only on PRs, guard the job or step in your workflow.
- To post PR comments, ensure the job has `permissions: pull-requests: write`.
- This action uses a sticky PR comment with `only_update: true`, so it updates an existing comment and does not create a new one if none exists.
