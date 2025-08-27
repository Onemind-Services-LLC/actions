# yq - Portable YAML Processor (Docker Action)

Run [`mikefarah/yq`](https://github.com/mikefarah/yq) in a pinned Docker container to create, read, update, delete, merge, and validate YAML.

## Inputs

- cmd: The exact command string to pass to `yq` (required).

## Outputs

- result: The complete result from the `yq` command (declared).

Note: This action runs the official `yq` container and prints output to the job logs. Capturing output into the `result` output requires the container entrypoint to write to `$GITHUB_OUTPUT`, which the upstream image does not do. Treat the output as log/console output; if you need to persist results, redirect to a file in your workflow.

## Usage

```yaml
jobs:
  example:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v5

      - name: Read a value
        uses: Onemind-Services-LLC/actions/actions/yq@master
        with:
          cmd: '.version'  # prints version from package.yaml

      - name: Update file in place
        uses: Onemind-Services-LLC/actions/actions/yq@master
        with:
          cmd: "-i '.image.tag = \"${{ github.sha }}\"' k8s/deploy.yaml"

      - name: Merge two files
        uses: Onemind-Services-LLC/actions/actions/yq@master
        with:
          cmd: 'ea . base.yaml overlay.yaml'

      - name: Validate YAML (no changes)
        uses: Onemind-Services-LLC/actions/actions/yq@master
        with:
          cmd: 'eval-all .'  # parses all YAML files under cwd
```

Security tips:
- The container image is pinned by digest. Prefer tag or commit pinning for calling actions as well.
- Third‑party actions in your workflows must be pinned to a version tag or commit SHA (no floating refs like `@master`).
- Do not echo secrets. Avoid putting secrets into YAML produced to logs.
