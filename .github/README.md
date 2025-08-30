# Reusable Workflows

Overview of reusable workflows published from this repository.

Consume via:

`uses: Onemind-Services-LLC/actions/.github/workflows/<file>.yml@master`

See also: [Actions Overview](../actions/README.md)

## Cypress Component Tests

- File: `.github/workflows/cypress-component-tests.yml`
- Purpose: Run Cypress component tests across a browser matrix with optional private npm auth via a GitHub App token.
- Permissions: `contents: read`.
- Inputs: `runs-on`, `browsers` (JSON array), `registry-url`, `registry-scope`, `working-directory`, `node-version`, `app-id`.
- Secrets: `private-key` (optional; GitHub App private key for npm auth).
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
      app-id: ${{ vars.APP_ID }}
    secrets:
      private-key: ${{ secrets.APP_PRIVATE_KEY }}
```

## JavaScript Quality Checks

- File: `.github/workflows/js-quality-checks.yml`
- Purpose: Orchestrates Prettier, ESLint, Browserslist DB lock, optional TypeScript type check and bundle integrity checks.
- Permissions: `contents: read`.
- Inputs: `runs-on`, `app-id` (optional; falls back to `vars.APP_ID`), `node-version`, `prettier-version`, `eslint-version`, `working-directory`, `patterns`, `eslint-args`, `eslint-config`, `run-prettier`, `run-eslint`, `run-browserslist`, `run-typescript`, `run-bundle-check`, `bundle-dist-path`, `bundle-command`, `tsconfig`, `tsc-args`.
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
      # Optionally override app-id; defaults to vars.APP_ID if set in caller repo
      app-id: ${{ vars.APP_ID }}
    secrets:
      private-key: ${{ secrets.APP_PRIVATE_KEY }}
```

## Next.js Bundle Analysis

- File: `.github/workflows/nextjs-bundle-analyzer.yml`
- Purpose: Generates Next.js bundle report on PRs, uploads artifact, compares with base, and comments results.
- Permissions: `contents: read`, `actions: read`, `pull-requests: write`.
- Inputs: `runs-on`, `node-version`, `registry-url`, `registry-scope`, `working-directory`, `install-command`, `build-command`, `extra-env`, `app-id`.
- Secrets: `private-key` (optional; GitHub App private key) and `github-token` (optional for artifact access/comments; falls back to App token when omitted).

## Docker Build + Push + Sign

- File: `.github/workflows/docker-build-push.yml`
- Purpose: Build with Buildx, generate tags/labels, optionally push, and keyless‑sign images.
- Permissions: `contents: read`, `id-token: write`.
- Inputs: `runs-on`, `push`, `image`, `meta-tags`, `annotations`, `build-args`, `build-secrets`, `cache-image`, `org-token`, `app-id`, `registry`.
- Secrets: `private-key` (optional; required when `org-token: 'true'`), `username`, `password`.
- Usage: `uses: Onemind-Services-LLC/actions/.github/workflows/docker-build-push.yml@master`

Notes:
- When `org-token: 'true'`, the workflow uses the provided GitHub App credentials (`inputs.app-id`, `secrets.private-key`) to mint an installation token and merges it into build secrets as `GITHUB_TOKEN=...`.
- Any user-provided `build-secrets` are merged with the generated token; duplicate keys are not de-duplicated (last write wins).

## Helm Charts CI

- File: `.github/workflows/helm-charts-ci.yml`
- Purpose: Lint/test charts on PRs and package/push on tags; optional keyless signing.
- Permissions: `contents: read`, `id-token: write`.
- Inputs: `runs-on`, `python-version`, `charts-dir`, `registry`, `oci-namespace`, `app-id`.
- Secrets: `docker-username`, `docker-password` (optional for authenticated push), `private-key` (optional; for App token).
- Usage: `uses: Onemind-Services-LLC/actions/.github/workflows/helm-charts-ci.yml@master`

## Python Package Publish (Token)

- File: `.github/workflows/python-publish.yml`
- Purpose: Build distributions (sdist/wheel) and publish to PyPI using an API token.
- Permissions: `contents: read`.
- Inputs: `runs-on`, `python-version`, `working-directory`, `build-command`, `skip-existing`, `app-id`.
- Secrets: `pypi-token` (required; project-scoped PyPI API token), `private-key` (optional; for App token).
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
- Permissions: `contents: read`, `checks: write`.
- Inputs: `app-id`, `plugin-name`, `plugin-configuration`, `netbox-version`, `python-version`, `runs-on`.
- Secrets: `private-key` (optional; GitHub App private key used to mint an installation token).
- Usage: `uses: Onemind-Services-LLC/actions/.github/workflows/netbox-plugin-tests.yml@master`

Notes:
- Internally reuses composite actions from this repo.
  - `actions/create-repo-token@master` to mint an installation token.
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
      app-id: ${{ vars.APP_ID }}
      plugin-name: my_netbox_plugin
      plugin-configuration: '{"enabled": true}'
      netbox-version: v4.3.6
      python-version: '3.12'
      runs-on: ubuntu-22.04-sh
    secrets:
      private-key: ${{ secrets.APP_PRIVATE_KEY }}
```

Security:
- The workflow avoids printing `PLUGINS_CONFIG` to logs to prevent secret leakage.

## CodeQL Analysis

- File: `.github/workflows/codeql-analysis.yml`
- Purpose: Initialize, optionally build, and run CodeQL analysis.
- Permissions: `contents: read`, `actions: read`, `security-events: write`.
- Inputs: `runs-on`, `languages`, `source-root`, `app-id`, `build-mode`, `build-command`, `queries`, `packs`, `config-file`, `tools`.
- Secrets: `private-key` (optional; for App token).

## Pre-commit Checks

- File: `.github/workflows/pre-commit.yml`
- Purpose: Run pre-commit hooks with a pinned action.
- Inputs: `runs-on`, `python-version`, `app-id`.
- Secrets: `private-key` (optional; for App token).

Notes:
- Internal CI for this repo lives in `.github/workflows/ci.yml` and is not reusable.

## Kibana Sourcemaps Upload

- File: `.github/workflows/kibana-sourcemaps-upload.yml`
- Purpose: Install/build a JS project and upload Next.js sourcemaps to Kibana/Elastic APM without requiring any repo scripts or npm deps.
- Permissions: `contents: read`, `packages: read`.
- Inputs: `runs-on`, `node-version`, `package-manager`, `working-directory`, `install`, `build`, `build-command`, `registry-url`, `registry-scope`, `app-id`, `base-url`, `kibana-url`, `build-dir`, `delete-existing`, `chunks-dirs` (default `chunks`, searched recursively).
- Secrets: `private-key` (optional; for App token), `kibana-api-key` (exported internally for upload).
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
      # Optional overrides
      # build-command: 'npm run build'
      # kibana-url: https://kibana.onemindservices.com/api/apm/sourcemaps
      # build-dir: .next/static
      # chunks-dirs: 'chunks'  # searched recursively
      # delete-existing: true
      app-id: ${{ vars.APP_ID }}
    secrets:
      private-key: ${{ secrets.APP_PRIVATE_KEY }}
      kibana-api-key: ${{ secrets.KIBANA_API_KEY }}
```
