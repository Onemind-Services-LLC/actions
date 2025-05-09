# NetBox Plugin Testing

This action provides a standardized way to test NetBox plugins. It sets up the necessary dependencies and runs plugin
tests against a specified version of NetBox.

## Features

- Automatically sets up PostgreSQL and Redis services
- Installs system dependencies
- Checks out the plugin repository and NetBox
- Handles plugin dependencies installation
- Configures NetBox for testing
- Validates database migrations
- Runs plugin tests

## Usage

Create a workflow file in your plugin repository (e.g., `.github/workflows/test.yml`):

```yaml
name: Tests

on:
  - push
  - pull_request

jobs:
  test:
    uses: Onemind-Services-LLC/actions/.github/workflows/netbox-plugin-tests.yml@master
    with:
      plugin_name: 'your-plugin-name'  # Repository/directory name with hyphens
      netbox_version: 'v4.2.9'  # Required: NetBox version to test against
      python_version: '3.12'  # Default: 3.12

    secrets:
      git_token: ${{ secrets.GIT_TOKEN }}
```

## Plugin Name Handling

The workflow automatically handles the conversion from hyphenated repository names (e.g., `netbox-portal`) to
underscore-separated Python module names (e.g., `netbox_portal`) for test execution.

## Requirements

Your plugin repository should have:

1. A standard Python package structure installable with `pip install -e .`
2. Tests in a module named `[plugin_name].tests` (with underscores)
3. A NetBox test configuration at `testing_configuration/configuration.py`

## Parameters

| Parameter        | Description                                                     | Required | Default |
|------------------|-----------------------------------------------------------------|----------|---------|
| `plugin_name`    | The name of the NetBox plugin (also used as the directory name) | Yes      | -       |
| `netbox_version` | NetBox version to test against                                  | Yes      | -       |
| `python_version` | Python version to use                                           | No       | `3.12`  |

## Secrets

| Secret      | Description                                     | Required |
|-------------|-------------------------------------------------|----------|
| `git_token` | GitHub token for accessing private repositories | Yes      |