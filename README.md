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

## Usage

To use these actions in your repository, reference them in your workflow file:

### NetBox Plugin Testing

```yaml
jobs:
  test:
    uses: Onemind-Services-LLC/actions/.github/workflows/netbox-plugin-tests.yml@master
    with:
      plugin-name: 'your_plugin_name'          # Required: Name of your NetBox plugin
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