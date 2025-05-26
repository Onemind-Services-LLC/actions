# Pre-commit Checks

A reusable GitHub Actions workflow for running pre-commit hooks across your organization's repositories. This workflow
provides consistent linting and code quality checks with minimal configuration.

## Features

- ✅ Runs all pre-commit hooks defined in `.pre-commit-config.yaml`
- 🚀 Built-in caching via official pre-commit action for faster execution
- 🔧 Configurable Python version
- 🎯 Uses official `pre-commit/action` for reliability
- 📦 Automatic pip caching for improved performance

## Usage

Create a workflow file in your repository (e.g., `.github/workflows/lint.yml`):

```yaml
name: Code Quality Checks

on:
  - push
  - pull_request

jobs:
  lint:
    uses: Onemind-Services-LLC/actions/.github/workflows/pre-commit.yml@master
    with:
      python-version: '3.12'         # Optional: Python version to use (default: 3.12)
      runner: 'ubuntu-22.04-sh'      # Optional: GitHub runner to use (default: ubuntu-22.04-sh)
```

## Parameters

| Parameter        | Description                           | Required | Default             | Type   |
|------------------|---------------------------------------|----------|---------------------|--------|
| `python-version` | Python version to use                 | No       | `'3.12'`            | string |
| `runner`         | GitHub runner to use for the workflow | No       | `'ubuntu-22.04-sh'` | string |

## Requirements

Your repository should have:

1. A `.pre-commit-config.yaml` file in the root directory
2. Python version specified must be available in GitHub Actions runners
3. Pre-commit hooks must be compatible with the specified Python version

## Configuration Examples

### Basic Usage

```yaml
jobs:
  lint:
    uses: Onemind-Services-LLC/actions/.github/workflows/pre-commit.yml@master
```

### With Custom Python Version

```yaml
jobs:
  lint:
    uses: Onemind-Services-LLC/actions/.github/workflows/pre-commit.yml@master
    with:
      python-version: '3.11'
```

### With Custom Runner

```yaml
jobs:
  lint:
    uses: Onemind-Services-LLC/actions/.github/workflows/pre-commit.yml@master
    with:
      runner: 'ubuntu-latest'
```

### Matrix Strategy with Multiple Python Versions

```yaml
jobs:
  lint:
    strategy:
      matrix:
        python-version: [ '3.9', '3.12', '3.11' ]
    uses: Onemind-Services-LLC/actions/.github/workflows/pre-commit.yml@master
    with:
      python-version: ${{ matrix.python-version }}
```

### Complete Workflow Example

```yaml
name: Code Quality and Tests

on:
  - push
  - pull_request

jobs:
  lint:
    name: Code Quality Checks
    uses: Onemind-Services-LLC/actions/.github/workflows/pre-commit.yml@master
    with:
      python-version: '3.12'
```

## Sample .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

exclude: 'migrations/.*|templates/.*'
```

## Troubleshooting

### Common Issues

**Problem**: Pre-commit hooks fail with "command not found"
**Solution**: Ensure all required tools are properly configured in your `.pre-commit-config.yaml` file.

**Problem**: Workflow runs on every file change
**Solution**: Use path filters in your trigger configuration to run only on relevant file changes.

**Problem**: Hooks are slow to run
**Solution**: The workflow automatically caches pre-commit environments and pip packages for faster subsequent runs.