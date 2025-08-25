# Django Test Runner

Run Django checks, apply migrations, collect static files, and execute tests with coverage reporting.

## Inputs

- **working-directory**: Directory containing `manage.py` (default: `.`).
- **django-settings-module**: Settings module to export for Django commands.
- **django-settings-module-key**: Env var name to export the settings module under (default: `DJANGO_SETTINGS_MODULE`).
- **verbosity**: Django command verbosity (default: `3`).
- **test-args**: Extra args appended to `manage.py test`.
- **coverage-args**: Extra args appended to `coverage xml`.

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

- Installs `coverage` via pip.
- Runs `makemigrations --check --dry-run` to enforce committed migrations.
- Runs `migrate -v <verbosity>`.
- Runs `collectstatic --noinput`.
- Runs `check -v <verbosity>`.
- Runs tests via `coverage run manage.py test` and generates `coverage.xml` via `coverage xml`.
- Optionally posts a Cobertura report comment using the `cobertura-report` composite action (pinned to 5monkeys) when `coverage-report: 'true'`.

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
    coverage-reporter-token: ${{ secrets.GIT_TOKEN }}
    coverage-minimum: '80'
    coverage-fail-below-threshold: 'true'
    coverage-show-line: 'true'
    coverage-show-branch: 'true'
    coverage-show-class-names: 'false'
    coverage-show-missing: 'true'
    coverage-only-changed-files: 'false'
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
