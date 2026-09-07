# Reusable Workflows

Overview of reusable workflows published from this repository.

Consume via:

`uses: Onemind-Services-LLC/actions/.github/workflows/<file>.yml@master`

See also: [Actions Overview](../actions/README.md)

## Authentication

Workflows that install private GitHub dependencies or inject a Docker build token accept the optional `GIT_TOKEN` secret. Pass it explicitly or use `secrets: inherit`; no GitHub App credentials or token-selection flags are needed. Dependency installs use `GIT_TOKEN` when supplied and otherwise fall back to `GITHUB_TOKEN`. Docker passes `GIT_TOKEN` directly as a build secret when supplied. Same-repository checkouts, artifacts, and PR comments use `GITHUB_TOKEN`.

```yaml
secrets:
  GIT_TOKEN: ${{ secrets.GIT_TOKEN }}
```

The token must have access to the private repositories or packages being installed. When using composite actions directly, pass it through their existing `github-token` or `npm-token` input.

## Cypress Component Tests

- File: `.github/workflows/cypress-component-tests.yml`
- Purpose: Run Cypress component tests across a browser matrix with GitHub Packages auth.
- Permissions: `contents: read`, `packages: read`.
- Inputs: `runs-on`, `browsers` (JSON array), `registry-url`, `registry-scope`, `working-directory`, `node-version`.
- Secrets: `GIT_TOKEN` (optional; private dependency access).
- Usage: `uses: Onemind-Services-LLC/actions/.github/workflows/cypress-component-tests.yml@master`

Example:

```yaml
permissions:
  contents: read
  packages: read

jobs:
  unit_test:
    uses: Onemind-Services-LLC/actions/.github/workflows/cypress-component-tests.yml@master
    with:
      runs-on: ubuntu-22.04-sh
      browsers: '["chrome","edge","firefox"]'
      registry-scope: '@onemind-services-llc'
      registry-url: 'https://npm.pkg.github.com'
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
  packages: read

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
- Inputs: `runs-on`, `node-version`, `registry-url`, `registry-scope`, `working-directory`, `install-command`, `build-command`, `extra-env`.
- Secrets: `GIT_TOKEN` (optional; private dependency access).

## Docker Build + Push + Sign

- File: `.github/workflows/docker-build-push.yml`
- Purpose: Build with Buildx, generate tags/labels, optionally push, and keyless‑sign images.
- Permissions: `contents: read`, `packages: read`, `id-token: write`.
- Inputs: `runs-on`, `push`, `image`, `meta-tags`, `annotations`, `build-args`, `build-secrets`, `cache-image`, `registry`.
- Secrets: `username`, `password`, `GIT_TOKEN` (optional; private build dependencies).
- Usage: `uses: Onemind-Services-LLC/actions/.github/workflows/docker-build-push.yml@master`

Notes:
- When supplied, `GIT_TOKEN` is passed directly into the Buildx secret named `github_token`. No token is generated or automatically injected when this secret is omitted.
- Any user-provided `build-secrets` are merged with `GIT_TOKEN`; duplicate keys are not de-duplicated (last write wins).
- Merged secrets are passed directly through the step output without creating a credentials file in the Docker build context.

Example with registry credentials and private build dependencies:

```yaml
permissions:
  contents: read
  packages: read
  id-token: write

jobs:
  build:
    uses: Onemind-Services-LLC/actions/.github/workflows/docker-build-push.yml@master
    with:
      registry: ghcr.io
      image: ghcr.io/example/app
      cache-image: ghcr.io/example/app:buildcache
    secrets:
      username: ${{ secrets.DOCKER_USERNAME }}
      password: ${{ secrets.DOCKER_PASSWORD }}
      GIT_TOKEN: ${{ secrets.GIT_TOKEN }}
```

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
- Inputs: `plugin-name`, `netbox-version`, `python-version`, `runs-on`, `coverage-minimum` (default `100`), `coverage-args` (default `--omit=*/migrations/*,*/templates/*,*/static/*,*/tests/*`).
- Secrets: `GIT_TOKEN` (optional; private dependency access).
- Usage: `uses: Onemind-Services-LLC/actions/.github/workflows/netbox-plugin-tests.yml@master`

Notes:
- Internally reuses composite actions from this repo.
  - `actions/python-setup-install@master` to set up Python and install deps for NetBox and the plugin.
  - `actions/django-test-runner@master` to run checks, migrations, collectstatic, and tests.
    Coverage is restricted to the plugin package (excludes NetBox itself).
- NetBox uses the plugin's `testing_configuration/configuration.py`, copied into its configuration directory and selected with `NETBOX_CONFIGURATION=netbox.configuration`. Put any `PLUGINS` and `PLUGINS_CONFIG` settings in that file.
- Private dependency authentication is scoped to the plugin install step through Git's runtime environment configuration; the token is not written into global Git configuration.
- Backing services use Redis (`redis:latest`) and Postgres (`postgres:17-alpine`) via our registry mirror.

Example:

```yaml
permissions:
  contents: read
  pull-requests: write

jobs:
  test:
    uses: Onemind-Services-LLC/actions/.github/workflows/netbox-plugin-tests.yml@master
    with:
      plugin-name: my_netbox_plugin
      netbox-version: v4.3.6
      python-version: '3.12'
      runs-on: ubuntu-22.04-sh
    secrets:
      GIT_TOKEN: ${{ secrets.GIT_TOKEN }}
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


## Gated container pipelines

The new workflows are independently callable with `workflow_call`. Pin them to
a reviewed commit SHA, and use `needs` in the caller to connect the pipeline.

| Workflow | Inputs | Outputs / gate |
| --- | --- | --- |
| `python-security.yml` | `source-directories`, optional Python/runner versions | Blocking Bandit, pip-audit and redacted Gitleaks; report artifacts |
| `container-build.yml` | `image`, `registry`, optional `build-args` | OCI `artifact-id` and `digest`; no registry push/cache write |
| `container-scan.yml` | `artifact-id`, `digest` | Exact artifact digest check and blocking HIGH/CRITICAL Trivy scan |
| `container-publish.yml` | `artifact-id`, `digest`, `image`, `registry`, `signer-identity` | Signed `image-ref` and `digest`; protected push only |

Build requires explicit `registry-username` and `registry-password` secrets,
plus `GIT_TOKEN` when private dependencies are needed. Publish requires only the registry credentials and
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
