# Reusable Workflows

Overview of reusable workflows published from this repository.

Consume via:

`uses: Onemind-Services-LLC/actions/.github/workflows/<file>.yml@master`

See also: [Actions Overview](../actions/README.md)

## Cypress Component Tests

- File: `.github/workflows/cypress-component-tests.yml`
- Purpose: Run Cypress component tests across a browser matrix with selectable GitHub Packages auth.
- Permissions: `contents: read`, `packages: read`.
- Inputs: `runs-on`, `browsers` (JSON array), `registry-url`, `registry-scope`, `working-directory`, `node-version`, `use-org-github-token`.
- Notes: If `use-org-github-token: true`, the workflow uses `secrets.ORG_GITHUB_TOKEN` when available and otherwise falls back to `GITHUB_TOKEN`.
- Usage: `uses: Onemind-Services-LLC/actions/.github/workflows/cypress-component-tests.yml@master`

Example:

```yaml
permissions:
  contents: read

jobs:
  unit_test:
    uses: Onemind-Services-LLC/actions/.github/workflows/cypress-component-tests.yml@master
    with:
      runs-on: ubuntu-22.04-sh
      browsers: '["chrome","edge","firefox"]'
      registry-scope: '@onemind-services-llc'
      registry-url: 'https://npm.pkg.github.com'
      use-org-github-token: true
    secrets: inherit
```

## JavaScript Quality Checks

- File: `.github/workflows/js-quality-checks.yml`
- Purpose: Orchestrates Prettier, ESLint, Browserslist DB lock, optional TypeScript type check and bundle integrity checks.
- Permissions: `contents: read`, `packages: read`.
- Inputs: `runs-on`, `node-version`, `prettier-version`, `eslint-version`, `working-directory`, `patterns`, `eslint-args`, `run-prettier`, `run-eslint`, `run-browserslist`, `run-typescript`, `run-bundle-check`, `bundle-dist-path`, `bundle-command`, `tsconfig`, `tsc-args`.
- Notes: Prettier/ESLint are executed via `npx` in their actions and do not install repository dependencies. If your project requires installs for other steps (TypeScript, bundle), configure those in the respective actions.
- Secrets: none required by default for these checks.

Example:

```yaml
permissions:
  contents: read

jobs:
  quality:
    uses: Onemind-Services-LLC/actions/.github/workflows/js-quality-checks.yml@master
    with:
      runs-on: ubuntu-22.04-sh
      node-version: '22.x'
```

## Next.js Bundle Analysis

- File: `.github/workflows/nextjs-bundle-analyzer.yml`
- Purpose: Generates Next.js bundle report on PRs, uploads artifact, compares with base, and comments results.
- Permissions: `contents: read`, `actions: read`, `packages: read`, `pull-requests: write`.
- Inputs: `runs-on`, `node-version`, `registry-url`, `registry-scope`, `working-directory`, `install-command`, `build-command`, `extra-env`, `use-org-github-token`.
- Notes: If `use-org-github-token: true`, the workflow uses `secrets.ORG_GITHUB_TOKEN` when available and otherwise falls back to `GITHUB_TOKEN`.

## Docker Build + Push + Sign

- File: `.github/workflows/docker-build-push.yml`
- Purpose: Build with Buildx, generate tags/labels, optionally push, and keyless‑sign images.
- Permissions: `contents: read`, `packages: read`, `id-token: write`.
- Inputs: `runs-on`, `push`, `image`, `meta-tags`, `annotations`, `build-args`, `build-secrets`, `cache-image`, `org-token`, `use-org-github-token`, `registry`.
- Secrets: `username`, `password`.
- Usage: `uses: Onemind-Services-LLC/actions/.github/workflows/docker-build-push.yml@master`

Notes:
- When `org-token: 'true'`, the workflow injects `github_token=...` into Buildx secrets.
- Set `use-org-github-token: true` to inject inherited `ORG_GITHUB_TOKEN` when available; otherwise it injects `GITHUB_TOKEN`.
- Any user-provided `build-secrets` are merged with the selected token; duplicate keys are not de-duplicated (last write wins).

## Helm Charts CI

- File: `.github/workflows/helm-charts-ci.yml`
- Purpose: Lint/test charts on PRs and package/push on tags; optional keyless signing.
- Permissions: `contents: read`, `id-token: write`.
- Inputs: `runs-on`, `python-version`, `charts-dir`, `registry`, `oci-namespace`.
- Secrets: `docker-username`, `docker-password` (optional for authenticated push).
- Usage: `uses: Onemind-Services-LLC/actions/.github/workflows/helm-charts-ci.yml@master`

## Python Package Publish (Token)

- File: `.github/workflows/python-publish.yml`
- Purpose: Build distributions (sdist/wheel) and publish to PyPI using an API token.
- Permissions: `contents: read`.
- Inputs: `runs-on`, `python-version`, `working-directory`, `build-command`, `skip-existing`.
- Secrets: `pypi-token` (required; project-scoped PyPI API token).
- Usage: `uses: Onemind-Services-LLC/actions/.github/workflows/python-publish.yml@master`

Example (tagged release):

```yaml
name: Release

on:
  release:
    types: [published]

permissions:
  contents: read

jobs:
  publish:
    uses: Onemind-Services-LLC/actions/.github/workflows/python-publish.yml@master
    with:
      python-version: '3.x'
      working-directory: '.'
      # skip-existing: 'true'
    secrets:
      pypi-token: ${{ secrets.PYPI_API_TOKEN }}
```

## NetBox Plugin Tests

- File: `.github/workflows/netbox-plugin-tests.yml`
- Purpose: Spin up Redis/Postgres, install NetBox + plugin, and run tests.
- Permissions: `contents: read`, `pull-requests: write`.
- Inputs: `plugin-name`, `plugin-configuration`, `netbox-version`, `python-version`, `runs-on`, `coverage-minimum` (default `100`), `coverage-args` (default `--omit=*/migrations/*,*/templates/*,*/static/*,*/tests/*`), `use-org-github-token`.
- Notes: If `use-org-github-token: true`, the workflow uses `secrets.ORG_GITHUB_TOKEN` when available and otherwise falls back to `GITHUB_TOKEN`.
- Usage: `uses: Onemind-Services-LLC/actions/.github/workflows/netbox-plugin-tests.yml@master`

Notes:
- Internally reuses composite actions from this repo.
  - `actions/python-setup-install@master` to set up Python and install deps for NetBox and the plugin.
  - `actions/django-test-runner@master` to run checks, migrations, collectstatic, and tests.
    Coverage is restricted to the plugin package (excludes NetBox itself).
- NetBox runs with `DJANGO_SETTINGS_MODULE=netbox.configuration` and a provided test configuration copied from `assets/netbox-plugin-tests/configuration.py`.
- Pass plugin settings via the `plugin-configuration` input as an inner config JSON string (only):
  - Example: `'{"github_token":"ghp_xxx"}'`
  - The workflow wraps this under your plugin name and writes a valid Python literal:
    `PLUGINS_CONFIG = {'<plugin-name>': {...}}` without stripping quotes.
  - Tip: In YAML, wrap the JSON string in single quotes and keep inner quotes as double quotes.
- Backing services use Redis (`redis:latest`) and Postgres (`postgres:17-alpine`) via our registry mirror.

Example:

```yaml
permissions:
  contents: read

jobs:
  test:
    uses: Onemind-Services-LLC/actions/.github/workflows/netbox-plugin-tests.yml@master
    with:
      plugin-name: my_netbox_plugin
      plugin-configuration: '{"enabled": true}'
      netbox-version: v4.3.6
      python-version: '3.12'
      runs-on: ubuntu-22.04-sh
      use-org-github-token: true
    secrets: inherit
```

Security:
- The workflow avoids printing `PLUGINS_CONFIG` to logs to prevent secret leakage.

## CodeQL Analysis

- File: `.github/workflows/codeql-analysis.yml`
- Purpose: Initialize, optionally build, and run CodeQL analysis.
- Permissions: `contents: read`, `actions: read`, `security-events: write`.
- Inputs: `runs-on`, `languages`, `source-root`, `build-mode`, `build-command`, `queries`, `packs`, `config-file`, `tools`.

## Pre-commit Checks

- File: `.github/workflows/pre-commit.yml`
- Purpose: Run pre-commit hooks with a pinned action.
- Inputs: `runs-on`, `python-version`.

Notes:
- Internal CI for this repo lives in `.github/workflows/ci.yml` and is not reusable.

## Kibana Sourcemaps Upload

- File: `.github/workflows/kibana-sourcemaps-upload.yml`
- Purpose: Install/build a JS project and upload Next.js sourcemaps to Kibana/Elastic APM without requiring any repo scripts or npm deps.
- Permissions: `contents: read`, `packages: read`.
- Inputs: `runs-on`, `node-version`, `package-manager`, `working-directory`, `install`, `build`, `build-command`, `registry-url`, `registry-scope`, `base-url`, `kibana-url`, `build-dir`, `delete-existing`, `chunks-dirs` (default `chunks`, searched recursively), `use-org-github-token`.
- Secrets: `kibana-api-key` (exported internally for upload).
- Notes: If `use-org-github-token: true`, the workflow uses `secrets.ORG_GITHUB_TOKEN` when available and otherwise falls back to `GITHUB_TOKEN`.
- Usage: `uses: Onemind-Services-LLC/actions/.github/workflows/kibana-sourcemaps-upload.yml@master`

Example:

```yaml
permissions:
  contents: read
  packages: read

jobs:
  upload_sourcemaps:
    uses: Onemind-Services-LLC/actions/.github/workflows/kibana-sourcemaps-upload.yml@master
    with:
      node-version: '22.x'
      package-manager: npm
      working-directory: '.'
      install: true
      build: true
      base-url: https://cloudmylab.com/_next/static
      use-org-github-token: true
      # Optional overrides
      # build-command: 'npm run build'
      # kibana-url: https://kibana.onemindservices.com/api/apm/sourcemaps
      # build-dir: .next/static
      # chunks-dirs: 'chunks'  # searched recursively
      # delete-existing: true
    secrets:
      kibana-api-key: ${{ secrets.KIBANA_API_KEY }}
```
