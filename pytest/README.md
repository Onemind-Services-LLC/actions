# Reusable Pytest Workflow

A GitHub Actions reusable workflow for running Python unit tests with pytest, coverage reporting, and automated PR
comments.

## Features

- 🐍 Configurable Python version support
- 🏃 Flexible runner selection
- 📊 Automated test coverage reporting
- 💬 PR comment integration with coverage summary
- 🔒 Secure dependency installation with Git token support
- 📦 Pip caching for faster builds
- 🌍 Environment file support for CI

## Usage

### Basic Usage

```yaml
name: Run Tests

on:
  pull_request:
    branches: [ main, dev ]
  push:
    branches: [ main, dev ]

jobs:
  test:
    uses: ./.github/workflows/pytest-workflow.yml
    secrets: inherit
```

### Advanced Usage with Custom Configuration

```yaml
name: Run Tests

on:
  pull_request:
    branches: [ main, dev ]
  push:
    branches: [ main, dev ]

jobs:
  test:
    uses: ./.github/workflows/pytest-workflow.yml
    with:
      python-version: '3.11'
      runner: 'ubuntu-latest'
    secrets: inherit
```

### Matrix Testing Across Multiple Python Versions

```yaml
name: Run Tests

on:
  pull_request:
    branches: [ main, dev ]
  push:
    branches: [ main, dev ]

jobs:
  test:
    strategy:
      matrix:
        python-version: [ '3.9', '3.10', '3.11', '3.12' ]
    uses: ./.github/workflows/pytest-workflow.yml
    with:
      python-version: ${{ matrix.python-version }}
    secrets: inherit
```

## Configuration

### Inputs

| Parameter        | Description                       | Required | Type   | Default          |
|------------------|-----------------------------------|----------|--------|------------------|
| `python-version` | Python version to use for testing | No       | string | `'3.12'`         |
| `runner`         | GitHub runner to use              | No       | string | `'ubuntu-22.04'` |

### Secrets

The workflow requires `secrets: inherit` to access the following secrets:

| Secret      | Description                                | Required |
|-------------|--------------------------------------------|----------|
| `GIT_TOKEN` | GitHub token for private repository access | Yes      |

## Project Structure Requirements

### Required Files

```
your-project/
├── requirements.txt          # Python dependencies
├── tests/                   # Test directory
│   ├── __init__.py
│   └── test_*.py           # Test files
├── app/                    # Application code (or your main package)
│   ├── __init__.py
│   └── *.py
└── env/                    # Environment files (optional)
    └── .env.ci            # CI environment file
```

### Dependencies

Your `requirements.txt` should include your project dependencies. The workflow automatically installs:

- `pytest` - Testing framework
- `pytest-cov` - Coverage plugin
- `pytest-mock` - Mocking plugin

## Environment Configuration

The workflow supports environment-specific configuration:

1. **CI Environment File**: If `env/.env.ci` exists, it will be copied to `env/.env` before running tests
2. **Custom Environment**: You can modify the setup step to handle different environment configurations

## Test Coverage

The workflow generates comprehensive coverage reports:

- **Terminal Output**: Coverage summary with missing lines
- **XML Report**: JUnit XML format for CI integration
- **PR Comments**: Automatic coverage comments on pull requests

### Coverage Comment Features

- Coverage percentage and trend
- Detailed file-by-file coverage breakdown
- Missing lines identification
- Comparison with the default branch (`dev`)

## Permissions

The workflow requires the following permissions:

- `pull-requests: write` - For posting coverage comments
- `contents: read` - For checking out the repository
- `id-token: write` - For secure token handling

## Best Practices

### Repository Setup

1. **Create the workflow file** in `.github/workflows/pytest-workflow.yml`
2. **Set up secrets** in your repository settings:
    - `GIT_TOKEN`: Personal access token or GitHub App token
3. **Configure branch protection** to require the workflow to pass

### Test Organization

```python
# tests/test_example.py
import pytest
from app.main import example_function


def test_example_function():
    """Test example function with valid input."""
    result = example_function("test")
    assert result == "expected_output"


def test_example_function_edge_case():
    """Test example function edge case."""
    with pytest.raises(ValueError):
        example_function(None)
```

### Coverage Configuration

Create a `.coveragerc` file to customize coverage settings:

```ini
[run]
source = app
omit =
    */tests/*
    */venv/*
    */__pycache__/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

## Troubleshooting

### Common Issues

1. **Missing requirements.txt**: Ensure your project has a `requirements.txt` file
2. **Import errors**: Check that your project structure matches the expected layout
3. **Permission errors**: Verify that `secrets: inherit` is included in your workflow call
4. **Coverage not found**: Ensure your tests are in the `tests/` directory and your app code is in `app/`

### Debug Mode

To enable debug logging, add this to your calling workflow:

```yaml
env:
  ACTIONS_STEP_DEBUG: true
```

## Examples

### Django Project

```yaml
name: Django Tests

on:
  pull_request:
    branches: [ main ]

jobs:
  test:
    uses: ./.github/workflows/pytest-workflow.yml
    with:
      python-version: '3.11'
      runner: 'ubuntu-latest'
    secrets: inherit
```

### FastAPI Project

```yaml
name: FastAPI Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    uses: ./.github/workflows/pytest-workflow.yml
    with:
      python-version: '3.12'
    secrets: inherit
```

## Contributing

When contributing to this workflow:

1. Test changes with a sample project
2. Update documentation for any new features
3. Ensure backward compatibility
4. Add appropriate error handling

## License

This workflow is provided as-is. Customize according to your project's needs.