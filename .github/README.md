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
- Inputs: `runs-on`, `app-id` (optional; falls back to `vars.APP_ID`), `node-version`, `prettier-version`, `eslint-version`, `working-directory`, `patterns`, `eslint-args`, `run-prettier`, `run-eslint`, `run-browserslist`, `run-typescript`, `run-bundle-check`, `bundle-dist-path`, `bundle-command`, `tsconfig`, `tsc-args`.
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
- Inputs: `runs-on`, `node-version`, `registry-url`, `registry-scope`, `working-directory`, `install-command`, `build-command`, `extra-env`, `app-id` (required).
- Secrets: `private-key` (required; GitHub App private key used to mint a token for artifact access and PR comments).

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
- Inputs: `app-id`, `plugin-name`, `plugin-configuration`, `netbox-version`, `python-version`, `runs-on`, `coverage-minimum` (default `80`), `coverage-args` (default `--omit=*/migrations/*,*/templates/*,*/static/*,*/tests/*`).
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

## Gated container pipelines

The new workflows are independently callable with `workflow_call`. Pin them to
a reviewed commit SHA, and use `needs` in the caller to connect the pipeline.

| Workflow | Inputs | Outputs / gate |
| --- | --- | --- |
| `python-security.yml` | `source-directories`, optional Python/runner versions | Blocking Bandit, pip-audit and redacted Gitleaks; report artifacts |
| `container-build.yml` | `image`, `registry`, `app-id`, `dependency-repositories`, optional `build-args` | OCI `artifact-id` and `digest`; no registry push/cache write |
| `container-scan.yml` | `artifact-id`, `digest` | Exact artifact digest check and blocking HIGH/CRITICAL Trivy scan |
| `container-publish.yml` | `artifact-id`, `digest`, `image`, `registry`, `signer-identity` | Signed `image-ref` and `digest`; protected push only |

Build requires explicit `registry-username`, `registry-password`, and
`app-private-key` secrets. Publish requires only the registry credentials and
`contents: read, id-token: write` permissions. Scan and source analysis have
read-only permissions and receive no deployment secrets. Supply read-only
registry credentials for base-image pulls; the server controls their scope.
The default runner is the existing `ubuntu-22.04-sh` Linux AMD64 label; override
`runs-on` for an isolated compatible runner.

The caller must gate publication on all source checks, tests, image scanning and
application smoke checks. The publisher does not infer scan success from an
artifact's existence. Pass `signer-identity` as the exact
`https://github.com/OWNER/actions/.github/workflows/container-publish.yml@SHA`
used in the workflow call; verification also binds the caller repository and SHA.

The builder exports OCI with SBOM and maximum BuildKit provenance. Consumers
retrieve an immutable artifact ID within the current run, not an arbitrary
cross-run artifact or mutable tag. Skopeo copies all manifests while preserving
digests. Publishing does not rebuild the image. It creates a SHA tag, signs and
verifies the digest, then promotes the branch/release alias. Artifacts expire in
three days; reports remain for 14 days.

Source scanning expects both runtime and development locks with exact registry
pins. VCS dependencies must use full commit SHAs; advisory coverage gaps are
reported explicitly. There are no silent scanner failures, automatic vulnerability
waivers, or `continue-on-error` gates. Install hooks in the Python setup composite
remain explicit shell commands for trusted workflow authors.

The legacy `docker-build-push.yml` now exposes its `digest` output and no longer
writes `merged_secrets.txt` into the caller's build context. Existing consumers
must update their pinned reference to receive those repairs. Prefer the separate
build/scan/publish workflows for new gated pipelines.

Build artifacts use GHA cache v2 scoped to image, architecture and ref. Validation
scopes are separate from protected-push scopes; the default branch's trusted
cache can be read as a fallback. Cache export failure only affects performance.
The Dockerfile should order dependency installation before application source,
use BuildKit secrets for private packages, and keep package caches out of final
layers. Cache mounts themselves are not exported by the GHA layer-cache backend.
