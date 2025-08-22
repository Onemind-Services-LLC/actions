# Reusable Workflows

Overview of reusable workflows published from this repository. Consume via:

`uses: Onemind-Services-LLC/actions/.github/workflows/<file>.yml@v1`

See also: [Actions Overview](../actions/README.md)

## Docker Build + Push + Sign

- File: `.github/workflows/docker-build-push.yml`
- Purpose: Build with Buildx, generate tags/labels, optionally push, and keyless‑sign images.
- Permissions: `contents: read`, `id-token: write` (for keyless signing).
- Inputs: `runner`, `push`, `image`, `meta-tags`, `annotations`, `build-args`, `build-secrets`, `cache-image`, `org-token`, `app-id`, `registry`.
- Secrets: `private-key`, `username`, `password`.
- Usage:
  `uses: Onemind-Services-LLC/actions/.github/workflows/docker-build-push.yml@v1`

Example usage with build secrets:

```yaml
permissions:
  contents: read
  id-token: write

jobs:
  build:
    uses: Onemind-Services-LLC/actions/.github/workflows/docker-build-push.yml@v1
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
```

## Helm Charts CI

- File: `.github/workflows/helm-charts-ci.yml`
- Purpose: Lint/test charts on PRs and package/push on tags; optional keyless signing.
- Permissions: `contents: read`, `id-token: write` (for signing).
- Inputs: `runner`, `python-version`, `charts-dir`, `registry`, `oci-namespace`.
- Secrets: `docker-username`, `docker-password` (optional for authenticated push).
- Usage:
  `uses: Onemind-Services-LLC/actions/.github/workflows/helm-charts-ci.yml@v1`

## NetBox Plugin Tests

- File: `.github/workflows/netbox-plugin-tests.yml`
- Purpose: Spin up Redis/Postgres, install NetBox + plugin, and run tests.
- Permissions: default; uses an installation token for private deps.
- Inputs: `plugin-name`, `netbox-version`, `python-version`, `runner`.
- Secrets/Vars: Requires GitHub App creds in caller repo (`vars.APP_ID`, `secrets.APP_PRIVATE_KEY`) via `create-repo-token`.
- Usage:
  `uses: Onemind-Services-LLC/actions/.github/workflows/netbox-plugin-tests.yml@v1`

## Next.js Bundle Analysis

- File: `.github/workflows/nextjs-bundle-analyzer.yml`
- Purpose: Build a Next.js app, upload bundle analysis, compare with base, and comment on PRs.
- Permissions: `contents: read`, `actions: read`, `pull-requests: write`.
- Inputs: `runner`, `node-version`, `registry-url`, `registry-scope`, `working-directory`, `install-command`, `build-command`, `extra-env`.
- Secrets: `github-token` (for artifact access and PR comments).
- Usage:
  `uses: Onemind-Services-LLC/actions/.github/workflows/nextjs-bundle-analyzer.yml@v1`

## Pre-commit Checks

- File: `.github/workflows/pre-commit.yml`
- Purpose: Run pre-commit hooks with cached Python setup.
- Permissions: default minimal.
- Inputs: `python-version`, `runner`.
- Usage:
  `uses: Onemind-Services-LLC/actions/.github/workflows/pre-commit.yml@v1`

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
      - uses: actions/checkout@v4
      - name: Yamllint
        uses: Onemind-Services-LLC/actions/actions/yamllint@v1
        with:
          config_file: .yamllint.yaml
          file_or_dir: .
          format: github
          fail-on-warnings: 'false'
```
