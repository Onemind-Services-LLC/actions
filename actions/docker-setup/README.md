# Docker Registry and Buildx Setup

Authenticate before starting the pinned mirrored BuildKit image.

Requires an Actions runner with Node 24 support (2.327.1 or newer).

## Inputs

| Input | Description | Default |
| --- | --- | --- |
| `registry` | Registry hostname for authentication | `Required` |
| `username` | Registry username | `Required` |
| `password` | Registry password or token | `Required` |
| `setup-buildx` | Set false for jobs that only need registry authentication | `true` |
| `driver-opts` | Newline-separated Buildx driver options | `image=registry.onemindservices.com/docker.io/moby/buildkit:buildx-stable-1@sha256:28a898719c18a33f4e8000685287fa36fd0dd9560c6440227d3a732d79bb41d8` |

## Usage

```yaml
- uses: Onemind-Services-LLC/actions/actions/docker-setup@master
  with:
    registry: registry.onemindservices.com
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_PASSWORD }}
```

Set `setup-buildx: false` for publication jobs that only need authentication.
Credentials are supplied by the caller; the action does not grant additional permissions.
