# Download Archived Artifacts

Validate artifact downloads and safely extract ZIPs without deprecated Node ZIP APIs.

Requires an Actions runner with Node 24 support (2.327.1 or newer).

## Inputs

| Input | Description | Default |
| --- | --- | --- |
| `name` | Select one artifact by name | `` |
| `artifact-ids` | Comma-separated immutable artifact IDs | `` |
| `pattern` | Glob pattern selecting artifact names | `` |
| `path` | Extraction directory, relative to the workspace or absolute | `.` |
| `merge-multiple` | Extract multiple artifacts into one directory instead of named subdirectories | `false` |
| `github-token` | Token with actions read permission; required for a different workflow run or repository | `` |
| `repository` | Repository containing the artifacts | `${{ github.repository }}` |
| `run-id` | Workflow run containing the artifacts | `${{ github.run_id }}` |

## Outputs

| Output | Description |
| --- | --- |
| `download-path` | Absolute directory containing the extracted artifacts |

## Usage

```yaml
- uses: Onemind-Services-LLC/actions/actions/artifact-download@master
  with:
    github-token: ${{ github.token }}
    run-id: ${{ needs.verify-ci.outputs.run-id }}
    pattern: image-*
    path: ${{ runner.temp }}/release-images
    merge-multiple: false
```

Requires Linux with Bash and Python 3.9 or newer. GitHub's Node 24 action downloads
ZIP archives and checks their artifact digests. Python extracts them with path
and symlink validation, avoiding the upstream Node ZIP extractor's deprecated
`Buffer()` API. Non-ZIP artifacts are rejected. Pair this with `artifact-upload`;
archives produced by older GitHub upload-artifact versions are also supported.

A single selected artifact extracts directly into `path`. Multiple artifacts use
named subdirectories unless `merge-multiple` is true. Uploaded file permissions
are not restored; extracted files use mode 0644. OCI tar archives preserve their
own internal image metadata. Downloads are staged under `RUNNER_TEMP` and cleaned
after extraction or failure. No image publication takes place.

Cross-run downloads need `actions: read` and an explicit `github-token`. For the
current run, the action can use the runner's artifact token without that input.
