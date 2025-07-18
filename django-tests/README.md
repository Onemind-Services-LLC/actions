# Django Unit Tests Reusable Workflow

A comprehensive GitHub Actions reusable workflow for running Django unit tests with configurable services including
PostgreSQL, Redis, MinIO, and InfluxDB.

## Features

- 🐍 **Configurable Python versions** - Test against different Python versions
- 🗄️ **Optional PostgreSQL** - Enable/disable PostgreSQL database service
- 🔄 **Optional Redis** - Enable/disable Redis caching service
- 📦 **Optional MinIO** - Enable/disable MinIO object storage service
- 📊 **Optional InfluxDB** - Enable/disable InfluxDB time series database
- 🏷️ **Version Control** - Specify exact versions for all services
- 📈 **Coverage Reporting** - Built-in coverage reporting with configurable thresholds
- 🔒 **Private Registry Support** - Works with private Docker registries
- 🎯 **Flexible Configuration** - Customize runners, and more

## Quick Start

### 1. Save the Reusable Workflow

Create `.github/workflows/django-unit-tests.yml` in your repository with the workflow content.

### 2. Create a Calling Workflow

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    uses: ./.github/workflows/django-unit-tests.yml
    with:
      python-version: '3.12'
      enable-postgresql: true
      enable-redis: true
      enable-minio: false
      enable-tsdb: false
      postgresql-version: 'latest'
      redis-version: 'latest'
    secrets: inherit
```

## Configuration Options

### Input Parameters

| Parameter            | Type    | Default             | Description                          |
|----------------------|---------|---------------------|--------------------------------------|
| `python-version`     | string  | `'3.12'`            | Python version to use for testing    |
| `enable-postgresql`  | boolean | `true`              | Enable PostgreSQL database service   |
| `enable-redis`       | boolean | `true`              | Enable Redis caching service         |
| `enable-minio`       | boolean | `false`             | Enable MinIO object storage service  |
| `enable-tsdb`        | boolean | `false`             | Enable InfluxDB time series database |
| `postgresql-version` | string  | `'latest'`          | PostgreSQL Docker image version      |
| `redis-version`      | string  | `'latest'`          | Redis Docker image version           |
| `minio-version`      | string  | `'latest'`          | MinIO Docker image version           |
| `influxdb-version`   | string  | `'latest'`          | InfluxDB Docker image version        |
| `runner`             | string  | `'ubuntu-22.04-sh'` | GitHub runner to use                 |

### Required Secrets

The workflow requires the following secrets to be available:

- `DOCKER_USERNAME` - Username for private Docker registry
- `DOCKER_PASSWORD` - Password for private Docker registry
- `GIT_TOKEN` - GitHub token for accessing private repositories

## Usage Examples

### Basic Usage

```yaml
jobs:
  test:
    uses: ./.github/workflows/django-unit-tests.yml
    with:
      python-version: '3.12'
      enable-postgresql: true
      enable-redis: false
      enable-minio: false
      enable-tsdb: false
    secrets: inherit
```

### With Specific Service Versions

```yaml
jobs:
  test:
    uses: ./.github/workflows/django-unit-tests.yml
    with:
      python-version: '3.11'
      enable-postgresql: true
      enable-redis: true
      enable-minio: true
      enable-tsdb: true
      postgresql-version: '15'
      redis-version: '7.2'
      minio-version: '2024.1.16'
      influxdb-version: '2.7.6-alpine'
    secrets: inherit
```

### Multiple Test Configurations

```yaml
jobs:
  test-minimal:
    uses: ./.github/workflows/django-unit-tests.yml
    with:
      python-version: '3.11'
      enable-postgresql: true
      enable-redis: false
      enable-minio: false
      enable-tsdb: false
    secrets: inherit

  test-full:
    uses: ./.github/workflows/django-unit-tests.yml
    with:
      python-version: '3.12'
      enable-postgresql: true
      enable-redis: true
      enable-minio: true
      enable-tsdb: true
    secrets: inherit
```

## Service Details

### PostgreSQL

- **Image**: `registry.onemindservices.com/docker.io/library/postgres`
- **Port**: 5432
- **Default Credentials**:
    - User: `postgres`
    - Password: `password`
    - Database: `app`

### Redis

- **Image**: `registry.onemindservices.com/docker.io/bitnami/redis`
- **Port**: 6379
- **Default Password**: `password`

### MinIO

- **Image**: `registry.onemindservices.com/docker.io/bitnami/minio`
- **Ports**: 9001 (API), 9002 (Console)
- **Default Credentials**:
    - User: `minioadmin`
    - Password: `minioadmin`

### InfluxDB

- **Image**: `registry.onemindservices.com/docker.io/library/influxdb`
- **Port**: 8086
- **Default Configuration**:
    - Username: `admin`
    - Password: `password`
    - Organization: `test`
    - Bucket: `things`
    - Token: `admin`

## Prerequisites

### Repository Structure

Your Django project should have the following structure:

```
your-repo/
├── .github/
│   └── workflows/
│       ├── django-unit-tests.yml  # The reusable workflow
│       └── test.yml               # Your calling workflow
├── requirements.txt               # Production dependencies
├── requirements_dev.txt           # Development dependencies
├── .env.test                      # Test environment variables
├── manage.py                      # Django management script
└── ... (your Django project files)
```

### Required Files

1. **requirements.txt** - Production dependencies
2. **requirements_dev.txt** - Development dependencies including `coverage`
3. **.env.test** - Test environment configuration

### Environment Variables

Create a `.env.test` file with your test configuration:

```env
DEBUG=True
SECRET_KEY=test-secret-key
DATABASE_URL=postgres://postgres:password@localhost:5432/app
REDIS_URL=redis://:password@localhost:6379/0
# Add other environment variables as needed
```

## Coverage Reporting

The workflow automatically generates coverage reports and integrates with pull requests. Coverage reports are only
generated for pull request events.

## Troubleshooting

### Common Issues

1. **Service Connection Issues**
    - Ensure health checks are passing
    - Check service versions are available in the registry
    - Verify network connectivity between services

2. **Authentication Issues**
    - Ensure `DOCKER_USERNAME` and `DOCKER_PASSWORD` secrets are set
    - Verify registry credentials are correct

3. **Coverage Reporting Issues**
    - Ensure `GIT_TOKEN` has appropriate permissions
    - Check that coverage files are being generated

### Debug Mode

To enable more verbose output, you can temporarily modify the workflow steps to include debug flags:

```yaml
- name: Run Tests
  run: coverage run manage.py test --debug-mode --buffer --timing --no-color --verbosity=2
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with different service configurations
5. Submit a pull request

## License

This workflow is provided as-is. Modify according to your needs.