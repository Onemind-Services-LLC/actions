# GitHub Actions

This repository contains a collection of reusable GitHub Actions and workflows for our organization.

## Available Actions

### NetBox Plugin Testing

A reusable workflow for testing NetBox plugins. This workflow sets up the necessary dependencies, including Redis and
PostgreSQL, and runs the plugin tests against a specified version of NetBox.

[View Documentation](./netbox-plugin-testing/README.md)

### Pre-commit Checks

A reusable workflow for running pre-commit hooks. This workflow sets up Python and executes pre-commit hooks to ensure
code quality and consistency across your repositories.

[View Documentation](./pre-commit-checks/README.md)

### Next.js Bundle Analysis

A reusable workflow to build a Next.js app, generate bundle analysis, upload an artifact, optionally compare to the base branch, and comment on PRs.

[View Documentation](./actions/nextjs-bundle-analyzer/README.md)

### NPM Install & Build (Composite)

Composite action to install and build a Node.js project using npm with caching and optional private registry auth.

[View Documentation](./actions/npm-install-build/README.md)

### Helm Charts CI

Reusable workflow to lint, test, package, and push Helm charts (on tags).

[View Documentation](./actions/helm-charts-ci/README.md)

### Cosign Sign (Composite)

Composite action to sign Docker images and Helm charts with Sigstore Cosign (key-based or keyless).

[View Documentation](./actions/cosign-sign/README.md)

### Docker Build, Push, and Sign (Composite)

Composite action to build with Buildx, optionally push, and keyless-sign Docker images.

[View Documentation](./actions/docker-build-push/README.md)

### Docker Build + Push + Sign (Reusable)

Reusable workflow that uses `docker/metadata-action` to generate tags/labels and then builds, pushes, and keyless-signs images via the composite.

[View Workflow](./.github/workflows/docker-build-push.yml)

## Usage

To use these actions in your repository, reference them in your workflow file:

### NetBox Plugin Testing

```yaml
jobs:
  test:
    uses: Onemind-Services-LLC/actions/.github/workflows/netbox-plugin-tests.yml@master
    with:
      plugin-name: 'your_netbox_plugin'        # Required: Name of your NetBox plugin
      netbox-version: 'v4.2.9'                 # Required: NetBox version to test against
      runner: 'ubuntu-22.04-sh'                # Optional: Runner environment (default: ubuntu-22.04-sh)
      python-version: '3.12'                   # Optional: Python version (default: 3.12)
```

### Pre-commit Checks

```yaml
jobs:
  pre-commit:
    uses: Onemind-Services-LLC/actions/.github/workflows/pre-commit.yml@master
    with:
      runner: 'ubuntu-22.04-sh'                # Optional: Runner environment (default: ubuntu-22.04-sh)
      python-version: '3.12'                   # Optional: Python version (default: 3.12)
```

### Next.js Bundle Analysis

```yaml
jobs:
  analyze:
    uses: Onemind-Services-LLC/actions/.github/workflows/nextjs-bundle-analyzer.yml@master
    permissions:
      contents: read
      actions: read
      pull-requests: write
    with:
      runner: 'ubuntu-22.04-sh'                # Optional: Runner (default: ubuntu-22.04-sh)
      node-version: '18'
      extra-env: |
        NEXT_PUBLIC_API_URL=${{ secrets.NEXT_PUBLIC_API_URL }}
      # Optional registry auth for private packages
      # registry-url: 'https://registry.npmjs.org'
      # registry-scope: '@your-scope'
    secrets:
      github-token: ${{ secrets.GITHUB_TOKEN }}

Note: This workflow now generates a GitHub App installation token internally for npm auth (via `create-repo-token`). Ensure the caller repository defines `APP_ID` (Repository variable) and `APP_PRIVATE_KEY` (Repository secret) for the GitHub App.
```
