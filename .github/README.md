# Reusable Workflows

Overview of reusable workflows published from this repository. Consume via:

`uses: Onemind-Services-LLC/actions/.github/workflows/<file>.yml@master`

See also: [Actions Overview](../actions/README.md)

## Cypress Component Tests

- File: `.github/workflows/cypress-component-tests.yml`
- Purpose: Run Cypress component tests across a browser matrix with optional private npm auth via a GitHub App token.
- Permissions: `contents: read`.
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
- Purpose: Run Cypress end-to-end tests across a browser matrix with optional private npm auth and caller-provided services.
- Permissions: `contents: read`.
- Inputs: `runs-on`, `browsers` (JSON array), `start`, `wait-on`, `wait-on-timeout`, `registry-url`, `registry-scope`, `working-directory`, `node-version`, `services` (JSON object), `app-id`.
- Secrets: `private-key` (GitHub App private key used to mint an installation token). You may also forward any additional secrets your `services` JSON references.
- Usage:
  `uses: Onemind-Services-LLC/actions/.github/workflows/cypress-e2e-tests.yml@master`

Notes:
- Services are caller-defined and passed as a JSON string via the `services` input. You can interpolate secrets in that JSON at the call site.
- You can set `needs`, `permissions`, and `strategy` at the call site as usual. This workflow already accepts a `browsers` JSON array and defines the matrix internally.

Example usage mirroring a typical stack:

```yaml
permissions:
  contents: read

jobs:
  unit_test:
    runs-on: ubuntu-22.04-sh
    steps:
      - uses: actions/checkout@v5
      - run: echo "run your unit tests here"

  e2e:
    name: End to End tests
    needs: [unit_test]
    uses: Onemind-Services-LLC/actions/.github/workflows/cypress-e2e-tests.yml@master
    with:
      runs-on: ubuntu-22.04-sh
      browsers: '["chrome","edge","firefox"]'
      start: npm run local:test
      wait-on: http://localhost:3000
      registry-scope: '@onemind-services-llc'
      registry-url: 'https://npm.pkg.github.com'
      services: >-
        {
          "postgres": {
            "image": "registry.onemindservices.com/docker.io/library/postgres:16",
            "credentials": {
              "username": "${{ secrets.DOCKER_USERNAME }}",
              "password": "${{ secrets.DOCKER_PASSWORD }}"
            },
            "env": {
              "POSTGRES_USER": "postgres",
              "POSTGRES_PASSWORD": "admin",
              "POSTGRES_DB": "app"
            },
            "ports": ["5432:5432"],
            "options": "--health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5"
          },
          "tsdb": {
            "image": "registry.onemindservices.com/docker.io/library/influxdb:2.7.6-alpine",
            "credentials": {
              "username": "${{ secrets.DOCKER_USERNAME }}",
              "password": "${{ secrets.DOCKER_PASSWORD }}"
            },
            "env": {
              "DOCKER_INFLUXDB_INIT_MODE": "setup",
              "DOCKER_INFLUXDB_INIT_USERNAME": "erp-influxdb",
              "DOCKER_INFLUXDB_INIT_PASSWORD": "password",
              "DOCKER_INFLUXDB_INIT_ORG": "test",
              "DOCKER_INFLUXDB_INIT_BUCKET": "things",
              "DOCKER_INFLUXDB_INIT_ADMIN_TOKEN": "admin"
            },
            "ports": ["8086:8086"],
            "options": "--health-cmd \"curl -f http://localhost:8086\" --health-interval 10s --health-timeout 5s --health-retries 30"
          },
          "redis": {
            "image": "registry.onemindservices.com/docker.io/bitnami/redis",
            "credentials": {
              "username": "${{ secrets.DOCKER_USERNAME }}",
              "password": "${{ secrets.DOCKER_PASSWORD }}"
            },
            "env": {
              "REDIS_PASSWORD": "password"
            },
            "ports": ["6379:6379"],
            "options": "--health-cmd \"redis-cli ping\" --health-interval 10s --health-timeout 5s --health-retries 30"
          },
          "minio": {
            "image": "registry.onemindservices.com/docker.io/bitnami/minio",
            "credentials": {
              "username": "${{ secrets.DOCKER_USERNAME }}",
              "password": "${{ secrets.DOCKER_PASSWORD }}"
            },
            "env": {
              "MINIO_ROOT_USER": "minioadmin",
              "MINIO_ROOT_PASSWORD": "minioadmin"
            },
            "ports": ["9000:9000"],
            "options": "--health-cmd \"curl -f http://localhost:9000/minio/health/live\" --health-interval 10s --health-timeout 5s --health-retries 30"
          },
          "server": {
            "image": "registry.onemindservices.com/zeus/python-master:dev",
            "credentials": {
              "username": "${{ secrets.DOCKER_USERNAME }}",
              "password": "${{ secrets.DOCKER_PASSWORD }}"
            },
            "env": {"SVC_TYPE": "test"},
            "ports": ["8000:8000"],
            "options": "--health-cmd \"curl -f http://localhost:8000/health/ping/\" --health-interval 10s --health-timeout 5s --health-retries 30"
          }
        }
    secrets:
      private-key: ${{ secrets.APP_PRIVATE_KEY }}
      DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
      DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}
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
