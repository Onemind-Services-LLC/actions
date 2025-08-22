# Cosign Sign (Composite Action)

Sign Docker images and Helm charts using Sigstore Cosign (keyless OIDC).

## Features

- Installs Cosign and signs either:
  - Docker images by tag@digest, or
  - Helm charts by deriving OCI refs from packaged `.tgz` files only.
- Uses keyless signing via OIDC. Ensure the calling job has `permissions: id-token: write`.

## Inputs

- mode: `docker` or `helm` (required).
- (Keyless only; no private key inputs.)

Docker-specific:
- docker-images: newline/space-separated list of `image:tag` to sign.
- docker-digest: `sha256:...` digest of the built image.

Helm-specific:
- registry: OCI registry host (e.g., `registry.example.com`).
- oci-namespace: OCI namespace/repo path (e.g., `charts`).
- chart-packages-dir: directory with packaged charts (`*.tgz`) to sign; derives refs as `oci://<registry>/<ns>/<name>:<version>`.

## Usage

### Sign Docker images

```yaml
- name: Sign image(s)
  uses: Onemind-Services-LLC/actions/actions/cosign-sign@master
  with:
    mode: docker
    docker-images: |
      ghcr.io/acme/app:latest
      ghcr.io/acme/app:${{ github.sha }}
    docker-digest: ${{ steps.build.outputs.digest }}
```

Keyless (OIDC) example:

```yaml
permissions:
  id-token: write

- name: Sign image(s) (keyless)
  uses: Onemind-Services-LLC/actions/actions/cosign-sign@master
  with:
    mode: docker
    docker-images: ghcr.io/acme/app:latest
    docker-digest: ${{ steps.build.outputs.digest }}
    # Keyless by default
```

### Sign Helm charts (from packaged files)

After packaging and pushing charts (e.g., to `oci://registry/ns`):

```yaml
- name: Sign packaged charts
  uses: Onemind-Services-LLC/actions/actions/cosign-sign@master
  with:
    mode: helm
    registry: registry.onemindservices.com
    oci-namespace: charts
    chart-packages-dir: ${{ runner.temp }}/helm-repo
    # Keyless by default
```

This action does not support signing Helm refs directly; it signs refs derived from packaged chart filenames (`<name>-<version>.tgz`).

## Notes

- For keyless, the calling job must grant `permissions: id-token: write` and the environment must support OIDC.
- The action does not push or build artifacts; it only signs references you specify/derive.
- For Docker, you must supply the digest that corresponds to the image tags you pass.
- For Helm, if you use `chart-packages-dir`, refs are derived from the package names (`<name>-<version>.tgz`).
