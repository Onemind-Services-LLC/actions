# Reusable Workflows

Overview of reusable workflows published from this repository. Consume via:

`uses: Onemind-Services-LLC/actions/.github/workflows/<file>.yml@master`

See also: [Actions Overview](../actions/README.md)

## Cypress Component Tests

- File: `.github/workflows/cypress-component-tests.yml`
- Purpose: Run Cypress component tests across a browser matrix with optional private npm auth via a GitHub App token.
- Permissions: `contents: read`, `id-token: write`.
- Inputs: `runs-on`, `browsers` (JSON array), `registry-url`, `registry-scope`, `working-directory`, `node-version`, `app-id`.
- Secrets: `private-key` (GitHub App private key used to mint an installation token for npm auth).
- Usage:
  `uses: Onemind-Services-LLC/actions/.github/workflows/cypress-component-tests.yml@master`

Example usage:

```yaml
permissions:
  contents: read

jobs:
  unit_test:
    name: Unit test
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

## Cypress E2E Tests

- File: `.github/workflows/cypress-e2e-tests.yml`
- Purpose: Run Cypress end-to-end tests across a browser matrix. Minimal design matching standard steps.
- Permissions: `contents: read`.
- Inputs: `runs-on`, `browsers` (JSON array), `start`, `wait-on`, `wait-on-timeout`, `registry-url`, `registry-scope`, `working-directory`, `node-version`, `app-id`.
- Secrets: `private-key` (GitHub App private key used to mint an installation token).
- Usage:
  `uses: Onemind-Services-LLC/actions/.github/workflows/cypress-e2e-tests.yml@master`

Example usage based on your sample:

```yaml
permissions:
  contents: read

jobs:
  e2e:
    name: End to End tests
    uses: Onemind-Services-LLC/actions/.github/workflows/cypress-e2e-tests.yml@master
    with:
      runs-on: ubuntu-22.04-sh
      browsers: '["chrome","edge","firefox"]'
      start: npm run local:test
      wait-on: http://localhost:3000
      registry-scope: '@onemind-services-llc'
      registry-url: 'https://npm.pkg.github.com'
    secrets:
      private-key: ${{ secrets.APP_PRIVATE_KEY }}
```




## Docker Build + Push + Sign

- File: `.github/workflows/docker-build-push.yml`
- Purpose: Build with Buildx, generate tags/labels, optionally push, and keyless‑sign images.
- Permissions: `contents: read`, `id-token: write` (for keyless signing).
- Inputs: `runs-on`, `push`, `image`, `meta-tags`, `annotations`, `build-args`, `build-secrets`, `cache-image`, `org-token`, `app-id`, `registry`.
- Secrets: `private-key`, `username`, `password`.
- Usage:
  `uses: Onemind-Services-LLC/actions/.github/workflows/docker-build-push.yml@master`

Example usage with build secrets:

```yaml
permissions:
  contents: read
  id-token: write

jobs:
  build:
    uses: Onemind-Services-LLC/actions/.github/workflows/docker-build-push.yml@master
    with:
      image: ghcr.io/acme/app
      cache-image: ghcr.io/acme/app:buildcache-${{ github.ref_name }}
      org-token: 'true'  # injects GITHUB_TOKEN=<org installation token>
      app-id: ${{ vars.APP_ID }}  # app id is not secret
      registry: ghcr.io           # registry host is not secret
      build-secrets: |
        NPM_TOKEN=${{ secrets.NPM_TOKEN }}
    secrets:
      private-key: ${{ secrets.ORG_APP_PRIVATE_KEY }}
      username: ${{ github.actor }}
      password: ${{ secrets.GITHUB_TOKEN }}
```

Notes:
- When `org-token: 'true'`, the workflow uses the provided GitHub App credentials (`inputs.app-id`, `secrets.private-key`) to mint an installation token and merges it into build secrets as `GITHUB_TOKEN=...`.
- Any user-provided `build-secrets` are merged with the generated token; duplicate keys are not de-duplicated (last write wins).

## Helm Charts CI

- File: `.github/workflows/helm-charts-ci.yml`
- Purpose: Lint/test charts on PRs and package/push on tags; optional keyless signing.
- Permissions: `contents: read`, `id-token: write` (for signing).
- Inputs: `runs-on`, `python-version`, `charts-dir`, `registry`, `oci-namespace`.
- Secrets: `docker-username`, `docker-password` (optional for authenticated push).
- Usage:
  `uses: Onemind-Services-LLC/actions/.github/workflows/helm-charts-ci.yml@master`

## Python Package Publish (Token)

- File: `.github/workflows/python-publish.yml`
- Purpose: Build distributions (sdist/wheel) and publish to PyPI using an API token.
- Permissions: `contents: read`.
- Inputs: `runs-on`, `python-version`, `working-directory`, `build-command`, `skip-existing`.
- Secrets: `pypi-token` (required; project-scoped PyPI API token).
- Behavior: Uses `user: __token__` with `password: ${{ secrets.pypi-token }}`.
- Usage:
  `uses: Onemind-Services-LLC/actions/.github/workflows/python-publish.yml@master`

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
- Permissions: default; uses an installation token for private deps.
- Inputs: `app-id`, `plugin-name`, `plugin-configuration`, `netbox-version`, `python-version`, `runs-on`.
- Secrets: `private-key` (GitHub App private key used to mint an installation token).
- Usage:
  `uses: Onemind-Services-LLC/actions/.github/workflows/netbox-plugin-tests.yml@master`

Notes:
- Internally reuses composite actions pinned in this repo to `@master`:
  - `actions/create-repo-token@master` to mint an installation token.
  - `actions/python-setup-install@master` to set up Python and install deps for NetBox and the plugin.
  - `actions/django-test-runner@master` to run checks, migrations, collectstatic, and tests.
- NetBox runs with `DJANGO_SETTINGS_MODULE=netbox.configuration` and a provided test configuration copied from `assets/netbox-plugin-tests/configuration.py`.
- Pass plugin settings via the `plugin-configuration` input to populate `PLUGINS_CONFIG`.
- Backing services use Redis (`redis:latest`) and Postgres (`postgres:17-alpine`) via our registry mirror.

Example usage:

```yaml
permissions:
  contents: read

jobs:
  test:
    uses: Onemind-Services-LLC/actions/.github/workflows/netbox-plugin-tests.yml@master
    with:
      app-id: ${{ vars.APP_ID }}
      plugin-name: my_netbox_plugin
      plugin-configuration: '{"my_netbox_plugin": {"enabled": true}}'
      netbox-version: v4.3.6
      python-version: '3.12'
      runs-on: ubuntu-22.04-sh
    secrets:
      private-key: ${{ secrets.APP_PRIVATE_KEY }}
```

## Next.js Bundle Analysis

- File: `.github/workflows/nextjs-bundle-analyzer.yml`
- Purpose: Build a Next.js app, upload bundle analysis, compare with base, and comment on PRs.
- Permissions: `contents: read`, `actions: read`, `pull-requests: write`.
- Inputs: `runs-on`, `node-version`, `registry-url`, `registry-scope`, `working-directory`, `install-command`, `build-command`, `extra-env`.
- Secrets: `github-token` (for artifact access and PR comments).
- Usage:
  `uses: Onemind-Services-LLC/actions/.github/workflows/nextjs-bundle-analyzer.yml@master`

## Pre-commit Checks

- File: `.github/workflows/pre-commit.yml`
- Purpose: Run pre-commit hooks with cached Python setup.
- Permissions: default minimal.
- Inputs: `python-version`, `runs-on`.
- Usage:
`uses: Onemind-Services-LLC/actions/.github/workflows/pre-commit.yml@master`

## ESLint/Prettier

- Prefer the composite actions for flexibility:
  - ESLint: `Onemind-Services-LLC/actions/actions/eslint-check@master`
  - Prettier: `Onemind-Services-LLC/actions/actions/prettier-check@master`
- Both composite actions auto-detect npm/yarn/pnpm and leverage the unified Node install/build action.

## CodeQL Analysis

- File: `.github/workflows/codeql-analysis.yml`
- Purpose: Initialize CodeQL, build, and upload results to GitHub code scanning. Caller provides a matrix of languages and passes a single language per job.
- Permissions: `contents: read`, `actions: read`, `security-events: write`.
- Inputs: `runs-on`, `languages` (single language per job), `source-root`, `build-mode` (`none` | `autobuild` | `manual`), `build-command`, `queries`, `packs`, `config-file`, `tools`.
- Usage:
  `uses: Onemind-Services-LLC/actions/.github/workflows/codeql-analysis.yml@master`

Example (caller provides language matrix):

```yaml
jobs:
  codeql:
    name: CodeQL
    strategy:
      fail-fast: false
      matrix:
        language: [ 'javascript-typescript', 'python' ]
    uses: Onemind-Services-LLC/actions/.github/workflows/codeql-analysis.yml@master
    with:
      runs-on: ubuntu-22.04-sh
      languages: ${{ matrix.language }}
      source-root: '.'
      build-mode: autobuild
      # For compiled languages with custom builds:
      # build-mode: manual
      # build-command: make -j
      # Optional:
      # queries: security-extended
```

## Browserslist Lock Check

- Prefer the composite action: `Onemind-Services-LLC/actions/actions/browserslist-lock-check@master`.
- Purpose: Run `update-browserslist-db` and fail if it modifies `package-lock.json`, `yarn.lock`, or `pnpm-lock.yaml`.

## JavaScript Quality Checks

- File: `.github/workflows/js-quality-checks.yml`
- Purpose: Run Prettier check, ESLint check, and Browserslist lock check in a single job.
- Permissions: `contents: read`.
- Inputs: `runs-on`, `node-version`, `working-directory`, `patterns`, `eslint-args`.
- Usage:
  `uses: Onemind-Services-LLC/actions/.github/workflows/js-quality-checks.yml@master`

Example usage:

```yaml
permissions:
  contents: read

jobs:
  js_quality:
    name: JS Quality
    uses: Onemind-Services-LLC/actions/.github/workflows/js-quality-checks.yml@master
    with:
      runs-on: ubuntu-22.04-sh
      node-version: '22.x'
      working-directory: '.'
      # patterns: '**/*.+(js|jsx|ts|tsx|json|css|scss)'
      # eslint-args: '.'
```

## Conventions

- Filenames use kebab‑case (e.g., `pre-commit.yml`).
- Jobs and steps use clear, Title Case names.
- Minimal permissions by default; elevate only as needed.
- Pin third‑party actions by version/commit; avoid `@master`.

## Local CI (Repo-only)

- File: `.github/workflows/ci.yml`
- Purpose: Lint YAML across this repository using the internal Yamllint composite action.
- Scope: Repo-only; guarded with `if: github.repository == 'Onemind-Services-LLC/actions'` to avoid running when this workflow is referenced elsewhere.
- Usage: Not reusable. Use the composite action directly in your repo instead (see below).

## Yamllint Action Usage

Use the composite action provided in this repo to lint YAML in your own workflows:

```yaml
jobs:
  yamllint:
    runs-on: ubuntu-22.04-sh
    steps:
      - uses: actions/checkout@v5
      - name: Yamllint
        uses: Onemind-Services-LLC/actions/actions/yamllint@master
        with:
          config_file: .yamllint.yaml
          file_or_dir: .
          format: github
          fail-on-warnings: 'false'
```
