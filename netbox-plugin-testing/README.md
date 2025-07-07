# NetBox Plugin Testing

A reusable GitHub Actions workflow for testing NetBox plugins. This workflow sets up the necessary dependencies and runs
plugin tests against a specified version of NetBox.

## Features

- 🐘 Automatically sets up PostgreSQL and Redis services
- 📦 Installs system dependencies
- 🔄 Checks out the plugin repository and NetBox
- 🛠️ Handles plugin dependencies installation
- ⚙️ Configures NetBox for testing
- 🗃️ Validates database migrations
- ✅ Runs plugin tests

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
      plugin-name: 'your_netbox_plugin'  # Required: Repository/directory name with underscores
      netbox-version: 'v4.2.9'           # Required: NetBox version to test against
      python-version: '3.12'             # Optional: Python version to use (default: 3.12)
      runner: 'ubuntu-22.04-sh'          # Optional: GitHub runner to use (default: ubuntu-22.04-sh)
    secrets:
      git-token: ${{ secrets.git-token }}
```

## Parameters

| Parameter        | Description                                                     | Required | Default             | Type   |
|------------------|-----------------------------------------------------------------|----------|---------------------|--------|
| `plugin-name`    | The name of the NetBox plugin (also used as the directory name) | Yes      | -                   | string |
| `netbox-version` | NetBox version to test against                                  | Yes      | -                   | string |
| `python-version` | Python version to use                                           | No       | `'3.12'`            | string |
| `runner`         | GitHub runner to use for the workflow                           | No       | `'ubuntu-22.04-sh'` | string |

## Secrets

| Secret      | Description                                     | Required |
|-------------|-------------------------------------------------|----------|
| `git-token` | GitHub token for accessing private repositories | Yes      |

## Requirements

Your plugin repository should have:

1. A standard Python package structure installable with `pip install -e .`
2. Tests in a module named `[plugin_name].tests` (with underscores)
3. A NetBox test configuration at `testing_configuration/configuration.py`

## Configuration Examples

### Basic Usage

```yaml
jobs:
  test:
    uses: Onemind-Services-LLC/actions/.github/workflows/netbox-plugin-tests.yml@master
    with:
      plugin-name: 'your_netbox_plugin'
      netbox-version: 'v4.2.9'
    secrets:
      git-token: ${{ secrets.git-token }}
```

### With Custom Python Version

```yaml
jobs:
  test:
    uses: Onemind-Services-LLC/actions/.github/workflows/netbox-plugin-tests.yml@master
    with:
      plugin-name: 'your_netbox_plugin'
      netbox-version: 'v4.2.9'
      python-version: '3.11'
    secrets:
      git-token: ${{ secrets.git-token }}
```

### With Custom Runner

```yaml
jobs:
  test:
    uses: Onemind-Services-LLC/actions/.github/workflows/netbox-plugin-tests.yml@master
    with:
      plugin-name: 'your_netbox_plugin'
      netbox-version: 'v4.2.9'
      runner: 'ubuntu-latest'
    secrets:
      git-token: ${{ secrets.git-token }}
```

### Matrix Strategy with Multiple NetBox Versions

```yaml
jobs:
  test:
    strategy:
      matrix:
        netbox-version: [ 'v4.2.1', 'v4.2.2', 'v4.2.3' ]
    uses: Onemind-Services-LLC/actions/.github/workflows/netbox-plugin-tests.yml@master
    with:
      plugin-name: 'your_netbox_plugin'
      netbox-version: ${{ matrix.netbox-version }}
    secrets:
      git-token: ${{ secrets.git-token }}
```

### Complete Workflow Example

```yaml
name: NetBox Plugin Tests

on:
  - push
  - pull_request

jobs:
  test:
    strategy:
      matrix:
        netbox-version: [ 'v4.2.9', 'v4.1.0' ]
        python-version: [ '3.11', '3.12' ]
    uses: Onemind-Services-LLC/actions/.github/workflows/netbox-plugin-tests.yml@master
    with:
      plugin-name: 'your_netbox_plugin'
      netbox-version: ${{ matrix.netbox-version }}
      python-version: ${{ matrix.python-version }}
    secrets:
      git-token: ${{ secrets.git-token }}
```

## Sample Testing Configuration

Create `testing_configuration/configuration.py` in your plugin repository:

```python
###################################################################
#  This file serves as a base configuration for testing purposes  #
#  only. It is not intended for production use.                   #
###################################################################

ALLOWED_HOSTS = ["*"]

DATABASE = {
    "NAME": "netbox",
    "USER": "netbox",
    "PASSWORD": "netbox",
    "HOST": "localhost",
    "PORT": "",
    "CONN_MAX_AGE": 300,
}

PLUGINS = [
    "your_netbox_plugin",  # Replace with your plugin name (with underscores)
]

PLUGINS_CONFIG = {  # type: ignore
    "your_netbox_plugin": {}  # Replace with your plugin configuration
}

REDIS = {
    "tasks": {
        "HOST": "localhost",
        "PORT": 6379,
        "PASSWORD": "",
        "DATABASE": 0,
        "SSL": False,
    },
    "caching": {
        "HOST": "localhost",
        "PORT": 6379,
        "PASSWORD": "",
        "DATABASE": 1,
        "SSL": False,
    },
}

SECRET_KEY = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

DEFAULT_PERMISSIONS = {}

ALLOW_TOKEN_RETRIEVAL = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True
}
```

## Troubleshooting

### Common Issues

**Problem**: Tests fail with database connection errors
**Solution**: Ensure your `testing_configuration/configuration.py` matches the service configuration.

**Problem**: Plugin not found during testing
**Solution**: Verify your `plugin-name` parameter matches your package name exactly (with underscores).

**Problem**: Migration errors during testing
**Solution**: Check that your plugin's migrations are compatible with the specified NetBox version.
