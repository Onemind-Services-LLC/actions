# Docker Build Workflow

A GitHub Actions reusable workflow for building, pushing, and signing Docker images with advanced caching and security
features.

## Features

- 🐳 Multi-image Docker builds with Buildx
- 🏷️ Automatic image tagging and metadata generation
- 🔒 Container image signing with Cosign
- 📦 Advanced Docker layer caching
- 🚀 Multi-registry support
- 🔐 Secure secret handling for private dependencies
- 🏃 Optimized build performance

## Usage

### Basic Usage

```yaml
name: Build and Push Docker Images

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    uses: Onemind-Services-LLC/actions/.github/workflows/docker-build.yml
    with:
      images: |
        myapp/backend
        myapp/api
    secrets: inherit
```

### Advanced Usage with Custom Configuration

```yaml
name: Build and Push Docker Images

on:
  push:
    branches: [ main, develop ]
    tags: [ 'v*' ]

jobs:
  build:
    uses: Onemind-Services-LLC/actions/.github/workflows/docker-build.yml
    with:
      images: |
        registry.onemindservices.com/myapp/backend
        registry.onemindservices.com/myapp/frontend
      file: './docker/Dockerfile'
      build-args: |
        NODE_ENV=production
        API_VERSION=v2
        BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
      cache-from: type=gha
      cache-to: type=gha,mode=max
      registry: registry.onemindservices.com
    secrets: inherit
```

### Multi-Stage Build with Different Registries

```yaml
name: Multi-Registry Build

on:
  push:
    branches: [ main ]

jobs:
  build-staging:
    uses: Onemind-Services-LLC/actions/.github/workflows/docker-build.yml
    with:
      images: |
        staging.registry.com/myapp/backend
      registry: staging.registry.com
    secrets: inherit

  build-production:
    uses: Onemind-Services-LLC/actions/.github/workflows/docker-build.yml
    with:
      images: |
        registry.onemindservices.com/myapp/backend
        ghcr.io/myorg/myapp/backend
      registry: registry.onemindservices.com
      cache-from: type=gha
      cache-to: type=gha,mode=max
    secrets: inherit
```

## Configuration

### Inputs

| Parameter    | Description                                                    | Required | Type   | Default                          |
|--------------|----------------------------------------------------------------|----------|--------|----------------------------------|
| `images`     | Docker images to build (multi-line string, one image per line) | Yes      | string | -                                |
| `file`       | Path to the Dockerfile                                         | No       | string | `'./Dockerfile'`                 |
| `build-args` | Build arguments (multi-line string, KEY=VALUE format)          | No       | string | `''`                             |
| `cache-from` | Cache source specification                                     | No       | string | `''`                             |
| `cache-to`   | Cache destination specification                                | No       | string | `''`                             |
| `registry`   | Docker registry to push images to                              | No       | string | `'registry.onemindservices.com'` |

### Secrets

The workflow requires `secrets: inherit` to access the following secrets:

| Secret               | Description                                | Required |
|----------------------|--------------------------------------------|----------|
| `DOCKER_USERNAME`    | Docker registry username                   | Yes      |
| `DOCKER_PASSWORD`    | Docker registry password/token             | Yes      |
| `GIT_TOKEN`          | GitHub token for private repository access | Yes      |
| `COSIGN_PRIVATE_KEY` | Cosign private key for image signing       | Yes      |
| `COSIGN_PASSWORD`    | Password for Cosign private key            | Yes      |

## Image Tagging Strategy

The workflow automatically generates tags based on the Git context:

- **Branch builds**: `branch-name`
- **Pull requests**: `pr-123`
- **Semantic versions**: `v1.2.3`, `1.2.3`, `1.2`, `1`, `latest`

### Tag Examples

```bash
# Branch: main
registry.onemindservices.com/myapp/backend:main

# Pull Request #42
registry.onemindservices.com/myapp/backend:pr-42

# Tag: v1.2.3
registry.onemindservices.com/myapp/backend:v1.2.3
registry.onemindservices.com/myapp/backend:1.2.3
registry.onemindservices.com/myapp/backend:1.2
registry.onemindservices.com/myapp/backend:1
registry.onemindservices.com/myapp/backend:latest
```

## Docker Build Arguments

### Basic Build Arguments

```yaml
with:
  build-args: |
    NODE_ENV=production
    API_VERSION=v2
    BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
```

### Dynamic Build Arguments

```yaml
with:
  build-args: |
    COMMIT_SHA=${{ github.sha }}
    BRANCH_NAME=${{ github.ref_name }}
    BUILD_NUMBER=${{ github.run_number }}
    REPOSITORY=${{ github.repository }}
```

## Caching Strategies

### GitHub Actions Cache

```yaml
with:
  cache-from: type=gha
  cache-to: type=gha,mode=max
```

### Registry Cache

```yaml
with:
  cache-from: type=registry,ref=myregistry.com/myapp/cache
  cache-to: type=registry,ref=myregistry.com/myapp/cache,mode=max
```

### Inline Cache

```yaml
with:
  cache-from: type=inline
  cache-to: type=inline
```

## Container Image Signing

The workflow automatically signs all built images using Cosign with the following features:

- **Keyless signing** with OIDC identity
- **Key-based signing** using private keys
- **Multiple image signing** in a single operation
- **Signature verification** ready

### Cosign Setup

1. **Generate a key pair**:

```bash
cosign generate-key-pair
```

2. **Add secrets to your repository**:
    - `COSIGN_PRIVATE_KEY`: Contents of `cosign.key`
    - `COSIGN_PASSWORD`: Password used to encrypt the private key

3. **Verify signatures**:

```bash
cosign verify --key cosign.pub registry.onemindservices.com/myapp/backend:main
```

## Dockerfile Best Practices

### Multi-Stage Dockerfile Example

```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Runtime stage
FROM node:18-alpine AS runtime
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .

# Build arguments
ARG NODE_ENV=production
ARG API_VERSION=unknown
ARG BUILD_DATE=unknown

# Labels for metadata
LABEL org.opencontainers.image.version="${API_VERSION}"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.source="https://github.com/myorg/myapp"

ENV NODE_ENV=${NODE_ENV}
EXPOSE 3000

CMD ["npm", "start"]
```

### Using Git Token for Private Dependencies

```dockerfile
# syntax=docker/dockerfile:1
FROM node:18-alpine

# Install git for private dependencies
RUN apk add --no-cache git

WORKDIR /app

# Configure git credentials (available as build secret)
RUN --mount=type=secret,id=github_token \
    git config --global url."https://$(cat /run/secrets/github_token)@github.com/".insteadOf "https://github.com/"

COPY package*.json ./
RUN npm ci --only=production

COPY . .
CMD ["npm", "start"]
```

## Security Considerations

### Repository Secrets Setup

1. **Docker Registry Credentials**:
    - `DOCKER_USERNAME`: Service account username
    - `DOCKER_PASSWORD`: Service account password or token

2. **GitHub Token**:
    - `GIT_TOKEN`: Personal access token with repo access
    - Scope: `repo` (for private repositories)

3. **Cosign Keys**:
    - `COSIGN_PRIVATE_KEY`: PEM-encoded private key
    - `COSIGN_PASSWORD`: Key encryption password

### Registry Security

```yaml
# Use specific registry URLs
registry: registry.onemindservices.com

# Avoid using 'latest' tag in production
tags: |
  type=semver,pattern={{version}}
  type=semver,pattern={{major}}.{{minor}}
```

## Troubleshooting

### Common Issues

1. **Authentication Failed**:
    - Verify `DOCKER_USERNAME` and `DOCKER_PASSWORD` are correct
    - Check registry URL format
    - Ensure service account has push permissions

2. **Build Context Too Large**:
    - Add `.dockerignore` file
    - Use multi-stage builds
    - Exclude unnecessary files

3. **Cosign Signing Failed**:
    - Verify `COSIGN_PRIVATE_KEY` format (PEM)
    - Check `COSIGN_PASSWORD` is correct
    - Ensure key pair was generated correctly

4. **Cache Issues**:
    - Use `type=gha,mode=max` for better cache efficiency
    - Clear cache with `actions/cache` action if needed

### Debug Mode

Enable debug logging:

```yaml
env:
  ACTIONS_STEP_DEBUG: true
  BUILDX_EXPERIMENTAL: 1
```

## Examples

### Microservices Build

```yaml
name: Microservices Build

on:
  push:
    branches: [ main, develop ]

jobs:
  build-services:
    strategy:
      matrix:
        service: [ api, worker, frontend ]
    uses: Onemind-Services-LLC/actions/.github/workflows/docker-build.yml
    with:
      images: |
        registry.onemindservices.com/myapp/${{ matrix.service }}
      file: ./services/${{ matrix.service }}/Dockerfile
      build-args: |
        SERVICE_NAME=${{ matrix.service }}
        BUILD_VERSION=${{ github.sha }}
      cache-from: type=gha
      cache-to: type=gha,mode=max
    secrets: inherit
```

### Conditional Registry Selection

```yaml
name: Conditional Build

on:
  push:
    branches: [ main, develop ]

jobs:
  build:
    uses: Onemind-Services-LLC/actions/.github/workflows/docker-build.yml
    with:
      images: |
        ${{ github.ref == 'refs/heads/main' && 'registry.onemindservices.com/myapp/backend' || 'staging.registry.com/myapp/backend' }}
      registry: ${{ github.ref == 'refs/heads/main' && 'registry.onemindservices.com' || 'staging.registry.com' }}
    secrets: inherit
```

## Performance Optimization

### Build Time Optimization

1. **Use build cache effectively**:

```yaml
cache-from: type=gha
cache-to: type=gha,mode=max
```

2. **Optimize Dockerfile layers**:

```dockerfile
# Copy dependency files first
COPY package*.json ./
RUN npm ci --only=production

# Copy source code last
COPY . .
```

3. **Use multi-stage builds**:

```dockerfile
FROM node:18-alpine AS dependencies
# Install dependencies

FROM node:18-alpine AS build
# Build application

FROM node:18-alpine AS runtime
# Runtime environment
```

## Contributing

When contributing to this workflow:

1. Test with various Docker configurations
2. Verify Cosign signing works correctly
3. Update documentation for new features
4. Ensure backward compatibility
5. Add appropriate error handling

## License

This workflow is provided as-is. Customize according to your project's needs.