# Reusable Pytest Workflow Documentation

## Overview

This reusable GitHub Actions workflow provides a standardized way to run pytest tests across multiple repositories. It
handles Python setup, dependency installation, environment configuration, test execution, and artifact collection.

## File Structure Requirements

Your repository must follow this structure for the workflow to work correctly:

```
your-repo/
├── .github/workflows/
│   └── pytest-reusable.yml          # The reusable workflow file
├── requirements.txt                  # Python dependencies
├── tests/                           # Test directory
│   ├── test_*.py                    # Test files
│   └── ...
├── app/                             # Source code directory (for coverage)
│   ├── __init__.py
│   └── ...
├── env/                             # Environment configuration
│   ├── .env.ci                      # CI environment file
│   └── .env                         # Runtime environment file
└── ...
```

## Workflow Features

### What it does:

1. **Environment Setup**: Sets up Python environment with specified version
2. **Dependency Caching**: Caches pip dependencies for faster builds
3. **Dependency Installation**: Installs requirements and pytest packages
4. **Environment Configuration**: Copies CI environment file to runtime location
5. **Test Execution**: Runs pytest with coverage reporting
6. **Artifact Collection**: Uploads test results and coverage reports

### Built-in Dependencies:

- `pytest`: Main testing framework
- `pytest-cov`: Coverage reporting
- `pytest-mock`: Mocking utilities

## Usage

### 1. Create the Reusable Workflow

Save the reusable workflow as `.github/workflows/pytest-reusable.yml` in your repository.

### 2. Call the Workflow

Create or update your main workflow file (e.g., `.github/workflows/ci.yml`):

```yaml
name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  unit_tests:
    name: Run unit tests
    uses: ./.github/workflows/pytest-reusable.yml
    with:
      python-version: '3.12'
      runner: 'ubuntu-22.04'
    secrets: inherit
```

## Input Parameters

| Parameter        | Description           | Type   | Required | Default          |
|------------------|-----------------------|--------|----------|------------------|
| `python-version` | Python version to use | string | No       | `'3.12'`         |
| `runner`         | GitHub runner type    | string | No       | `'ubuntu-22.04'` |

## Required Secrets

The workflow uses `secrets: inherit` which means all secrets from the calling workflow are automatically passed to the
reusable workflow. You need to ensure your repository has the following secret configured:

| Secret      | Description                                | Required |
|-------------|--------------------------------------------|----------|
| `GIT_TOKEN` | GitHub token for private repository access | Yes      |

## Fixed Configuration

The workflow uses these fixed paths and configurations:

- **Requirements File**: `requirements.txt`
- **Test Directory**: `tests/`
- **Coverage Source**: `app`
- **Environment Source**: `env/.env.ci`
- **Environment Destination**: `env/.env`
- **Pytest Arguments**: `--junitxml=pytest.xml --cov-report=term-missing:skip-covered --cov=app tests/`

## Artifacts

The workflow automatically uploads:

1. **Test Results**: `pytest.xml` (JUnit format)
2. **Coverage Reports**: `.coverage` file

These artifacts are available for download from the GitHub Actions run page.

## Examples

### Basic Usage

```yaml
jobs:
  test:
    uses: ./.github/workflows/pytest-reusable.yml
    secrets: inherit
```

### With Custom Python Version

```yaml
jobs:
  test:
    uses: ./.github/workflows/pytest-reusable.yml
    with:
      python-version: '3.11'
    secrets: inherit
```

### With Custom Runner

```yaml
jobs:
  test:
    uses: ./.github/workflows/pytest-reusable.yml
    with:
      runner: 'ubuntu-22.04-sh'
    secrets: inherit
```

### Matrix Testing (Multiple Python Versions)

```yaml
jobs:
  test:
    strategy:
      matrix:
        python-version: [ '3.11', '3.12', '3.13' ]
    uses: ./.github/workflows/pytest-reusable.yml
    with:
      python-version: ${{ matrix.python-version }}
    secrets: inherit
```

## Prerequisites

### Repository Setup:

1. Create `requirements.txt` with your project dependencies
2. Organize tests in `tests/` directory
3. Place source code in `app/` directory
4. Create `env/.env.ci` for CI environment variables
5. Set up `GIT_TOKEN` secret in repository settings

### Environment File:

Create `env/.env.ci` with necessary environment variables for testing:

```env
# Example CI environment variables
DATABASE_URL=sqlite:///test.db
DEBUG=true
TESTING=true
```

## Troubleshooting

### Common Issues:

1. **Missing requirements.txt**: Ensure `requirements.txt` exists in repository root
2. **Test discovery**: Make sure test files follow pytest naming conventions (`test_*.py`)
3. **Coverage issues**: Verify `app/` directory contains your source code
4. **Environment setup**: Check if `env/.env.ci` exists and contains required variables
5. **Token issues**: Ensure `GIT_TOKEN` secret is set and has appropriate permissions

### Debug Steps:

1. Check workflow logs in GitHub Actions tab
2. Verify file structure matches requirements
3. Test locally with same pytest command
4. Validate environment file format

## Benefits

1. **Consistency**: Standardized testing across all repositories
2. **Maintainability**: Single source of truth for test configuration
3. **Efficiency**: Cached dependencies reduce build times
4. **Flexibility**: Easy to customize Python version and runner
5. **Artifacts**: Automatic collection of test results and coverage
6. **Reliability**: Uses latest GitHub Actions versions
7. **Simplified Secrets**: Uses `secrets: inherit` for easier secret management

## Migration from Existing Workflows

If you have existing pytest workflows, follow these steps:

1. Copy your current workflow logic to match the expected structure
2. Update file paths to match the fixed configuration
3. Replace your existing workflow with a call to the reusable workflow
4. Test the migration with a pull request

## Support

For issues or questions:

1. Check the troubleshooting section
2. Review workflow logs
3. Verify repository structure
4. Test locally with equivalent commands