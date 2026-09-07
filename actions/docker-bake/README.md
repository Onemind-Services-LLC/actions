# Docker Bake

Build a caller-owned Bake graph and expose its selected image digest.

Requires an Actions runner with Node 24 support (2.327.1 or newer).

## Inputs

| Input | Description | Default |
| --- | --- | --- |
| `files` | Newline-separated Bake definition files | `Required` |
| `source` | Bake source context; use the checkout by default | `.` |
| `target` | Target whose containerimage.digest should be returned | `` |
| `targets` | Targets to build; empty uses the Bake default group | `` |
| `allow` | Newline-separated explicit Buildx entitlements | `` |
| `set` | Newline-separated Bake target overrides | `` |
| `push` | Push output to registries; false preserves caller-selected outputs | `false` |

## Outputs

| Output | Description |
| --- | --- |
| `metadata` | Complete Buildx metadata JSON; avoid placing it in a process environment variable |
| `digest` | Image digest for the selected target, or empty when no target is selected |

## Usage

```yaml
- uses: Onemind-Services-LLC/actions/actions/docker-setup@master
  with:
    registry: registry.onemindservices.com
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_PASSWORD }}
- uses: Onemind-Services-LLC/actions/actions/docker-bake@master
  id: build
  with:
    files: docker-bake.hcl
    target: app
    allow: fs.write=${{ runner.temp }}
    set: app.output=type=oci,dest=${{ runner.temp }}/image.tar
    push: false
```

The caller owns the Bake graph, cache scopes, tags, attestations, and job dependencies.
Run Docker setup first. `target` selects a digest output; use `targets` to override
the targets being built. Prefer the small `digest` output over placing complete
metadata in an environment variable, which can exceed the operating system limit.
This action does not publish unless explicitly requested.
