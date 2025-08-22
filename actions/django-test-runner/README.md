# Django Test Runner

Run Django checks, apply migrations, collect static files, and execute tests with coverage reporting.

## Inputs

- **working-directory**: Directory containing `manage.py` (default: `.`).
- **django-settings-module**: Optional `DJANGO_SETTINGS_MODULE` to export for commands.
- **python-executable**: Python executable to use (default: `python`).
- **verbosity**: Django command verbosity (default: `3`).
- **test-args**: Extra args appended to `manage.py test`.
- **coverage-args**: Extra args appended to `coverage xml`.

## What it does

- Ensures `coverage` is installed (installs via pip if missing).
- Runs `makemigrations --check --dry-run` to enforce committed migrations.
- Runs `migrate -v <verbosity>`.
- Runs `collectstatic --noinput`.
- Runs `check -v <verbosity>`.
- Runs tests via `python -m coverage run manage.py test` and generates `coverage.xml` via `python -m coverage xml`.

## Examples

### Basic

```yaml
- name: Django Test Runner
  uses: OWNER/REPO/actions/django-test-runner@v1
```

### With settings module and extra test args

```yaml
- name: Django Test Runner
  uses: OWNER/REPO/actions/django-test-runner@v1
  with:
    django-settings-module: myproj.settings.test
    test-args: "--pattern='test_*.py'"
```

### In a subdirectory and custom Python

```yaml
- name: Django Test Runner
  uses: OWNER/REPO/actions/django-test-runner@v1
  with:
    working-directory: backend
    python-executable: python3
    verbosity: '2'
```

## Notes

- Assumes dependencies and services (e.g., database, cache) are available. Use your workflow to provision services before invoking this action.
- If you rely on environment variables (database URLs, secrets), set them at the job or step level of your workflow.
- Uses `bash` shell and `python -m coverage` to ensure the interpreter’s environment is used.
