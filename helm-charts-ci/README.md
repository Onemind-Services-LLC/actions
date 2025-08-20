# Helm Charts CI

Reusable workflow to lint, test, package, push, and keyless-sign Helm charts.

## Features

- Lints changed charts using `helm/chart-testing-action`.
- Packages charts under a configurable glob (default `charts/*/`).
- Pushes packaged charts to an OCI registry on tag builds.
- Skips packaging and pushing when no charts changed (based on chart-testing).
- Always signs pushed charts using Cosign (keyless OIDC).
- Configurable runner, Python version, chart-testing action version, registry, and namespace.

## Usage

```yaml
name: CI

on:
  push: {}
  pull_request: {}

jobs:
  charts:
    uses: Onemind-Services-LLC/actions/.github/workflows/helm-charts-ci.yml@master
    with:
      runner: 'ubuntu-22.04-sh'
      python-version: '3.x'
      ct-version: 'v2.7.0'
      charts-dir: 'charts'
      registry: 'registry.onemindservices.com'
      oci-namespace: 'charts'
    secrets:
      docker-username: ${{ secrets.DOCKER_USERNAME }}
      docker-password: ${{ secrets.DOCKER_PASSWORD }}
```

## Inputs

- runner: GitHub runner label (default `ubuntu-22.04-sh`).
- python-version: Python version for chart-testing (default `3.x`).
- ct-version: Version of `helm/chart-testing-action` (default `v2.7.0`).
- charts-dir: Directory containing chart subfolders (default `charts`).
- registry: OCI registry hostname (default `registry.onemindservices.com`).
- oci-namespace: OCI namespace/repo path (default `charts`).

## Secrets

- docker-username: Username for registry login.
- docker-password: Password/Token for registry login.

## Notes

- The release job runs only for tag refs and depends on lint-test. It skips login, packaging, pushing, and signing if no charts changed.
- Charts are signed (keyless OIDC) by OCI reference `oci://<registry>/<namespace>/<name>:<version>` after push.
- This workflow requests `id-token: write` to enable keyless signing.
- The default target branch for chart-testing is the repository default branch.
- Ensure `helm` and `chart-testing` setup steps meet your environment needs.
