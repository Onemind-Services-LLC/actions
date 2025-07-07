# Docker Build Workflow

A reusable GitHub Actions workflow for building, pushing, and signing Docker images with configurable parameters.

## Features

- 🐳 **Multi-image support**: Build and push multiple Docker images
- 🔧 **Configurable build arguments**: Pass custom build arguments
- 🚀 **Caching support**: Optimize builds with registry caching
- 🔐 **Image signing**: Automatic Cosign image signing
- 📦 **Streamlined configuration**: Essential parameters with sensible defaults

## Usage

### Basic Usage

```yaml
name: Build and Deploy

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: echo "Running tests..."

  docker-build:
    uses: ./.github/workflows/docker-build.yml
    needs: unit-tests
    with:
      images: |
        registry.onemindservices.com/my-app/backend
        registry.onemindservices.com/my-app/frontend
```

### Advanced Usage

```yaml
jobs:
  docker-build:
    uses: ./.github/workflows/docker-build.yml
    with:
      images: |
        registry.onemindservices.com/zeus/python-master
        ghcr.io/myorg/myapp
      file: './docker/Dockerfile.prod'
      build-args: |
        NODE_ENV=production
        API_URL=https://api.example.com
        DEBUG=false
      cache-from: type=registry,ref=registry.onemindservices.com/zeus/python-master:cache
      cache-to: type=registry,ref=registry.onemindservices.com/zeus/python-master:cache,mode=max
```

## Configuration Parameters

### Required Inputs

| Parameter | Type     | Description                                                    |
|-----------|----------|----------------------------------------------------------------|
| `images`  | `string` | Docker images to build (multi-line string, one image per line) |

### Optional Inputs

| Parameter    | Type     | Default                                             | Description                                           |
|--------------|----------|-----------------------------------------------------|-------------------------------------------------------|
| `file`       | `string` | `./Dockerfile`                                      | Path to the Dockerfile                                |
| `build-args` | `string` | `SERVICE_VERSION=${{ steps.meta.outputs.version }}` | Build arguments (multi-line string, KEY=VALUE format) |
| `cache-from` | `string` | `''`                                                | Cache source specification                            |
| `cache-to`   | `string` | `''`                                                | Cache destination specification                       |

## Fixed Configuration

The workflow uses the following fixed settings:

- **Runner**: `ubuntu-22.04`
- **Registry**: `registry.onemindservices.com`
- **Build Arguments**: Default includes `SERVICE_VERSION` from metadata

## Examples

### Multi-Image Build

```yaml
with:
  images: |
    registry.onemindservices.com/app/backend
    registry.onemindservices.com/app/frontend
    registry.onemindservices.com/app/worker
```

### Custom Build Arguments

```yaml
with:
  build-args: |
    NODE_ENV=production
    API_VERSION=v2
    BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
    COMMIT_SHA=${{ github.sha }}
    SERVICE_VERSION=${{ steps.meta.outputs.version }}
```

**Note**: If you provide custom build-args, you need to include `SERVICE_VERSION` manually if required by your
Dockerfile.

### Registry Caching

```yaml
with:
  cache-from: type=registry,ref=myregistry.com/myapp:cache
  cache-to: type=registry,ref=myregistry.com/myapp:cache,mode=max
```

### Different Dockerfile

```yaml
with:
  file: './docker/Dockerfile.production'
```

## Outputs

The workflow provides the following outputs that can be used in downstream jobs:

| Output     | Description                      |
|------------|----------------------------------|
| `tags`     | Generated Docker tags            |
| `digest`   | Docker image digest              |
| `metadata` | Complete metadata in JSON format |

### Using Outputs

```yaml
jobs:
  docker-build:
    uses: ./.github/workflows/docker-build.yml
    with:
      images: registry.onemindservices.com/my-app
    secrets:
      DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
      DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}
      GIT_TOKEN: ${{ secrets.GIT_TOKEN }}
      COSIGN_PRIVATE_KEY: ${{ secrets.COSIGN_PRIVATE_KEY }}
      COSIGN_PASSWORD: ${{ secrets.COSIGN_PASSWORD }}

  deploy:
    needs: docker-build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy with digest
        run: |
          echo "Deploying image with digest: ${{ needs.docker-build.outputs.digest }}"
          echo "Tags: ${{ needs.docker-build.outputs.tags }}"
```

## Image Tagging Strategy

The workflow uses the following tagging strategy:

- **Branch builds**: `branch-name`
- **Pull requests**: `pr-123`
- **Semantic versions**: `v1.0.0`, `v1.0`, `v1`
- **SHA tags**: `branch-sha123456`

## Security Features

### Image Signing

All images are automatically signed using Cosign. The workflow requires:

- `COSIGN_PRIVATE_KEY`: Your Cosign private key
- `COSIGN_PASSWORD`: Password for the private key

### Registry Authentication

The workflow is configured to authenticate with `registry.onemindservices.com` using:

- `DOCKER_USERNAME`: Registry username
- `DOCKER_PASSWORD`: Registry password

### Secrets Management

All sensitive information is passed through GitHub secrets for security.

## Troubleshooting

### Common Issues

1. **Authentication failures**: Ensure Docker registry credentials are correct for `registry.onemindservices.com`
2. **Missing secrets**: Verify all required secrets (including Cosign keys) are set in your repository
3. **Build failures**: Check Dockerfile path and build arguments
4. **Signing failures**: Ensure Cosign private key and password are properly configured
5. **Build args issues**: If using custom build-args, ensure you include `SERVICE_VERSION` if your Dockerfile expects it

### Debug Mode

To enable debug logging, add the following to your workflow:

```yaml
env:
  ACTIONS_STEP_DEBUG: true
```

## File Structure

```
.github/
└── workflows/
    ├── docker-build.yml          # This reusable workflow
```

## Contributing

When modifying this workflow:

1. Test changes thoroughly with real builds
2. Update this documentation
3. Ensure all secrets are properly configured
4. Test image signing functionality
5. Verify multi-image builds work correctly