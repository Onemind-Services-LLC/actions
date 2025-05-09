# GitHub Actions

This repository contains a collection of reusable GitHub Actions and workflows for our organization.

## Available Actions

### NetBox Plugin Testing

A reusable workflow for testing NetBox plugins. This workflow sets up the necessary dependencies, including Redis and PostgreSQL, and runs the plugin tests against a specified version of NetBox.

[View Documentation](./netbox-plugin-testing/README.md)

## Usage

To use these actions in your repository, reference them in your workflow file:

```yaml
jobs:
  test:
    uses: Onemind-Services-LLC/actions/.github/workflows/netbox-plugin-tests.yml@main
    with:
      plugin_name: 'your-plugin-name'
      netbox_version: 'v4.2.9'  # Required: NetBox version to test against
      python_version: '3.12'  # Default: 3.12
```
