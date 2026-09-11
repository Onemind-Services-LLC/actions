# Upload Archived Artifact

Upload named ZIP artifacts while preserving their paths and retention policy.

Requires an Actions runner with Node 24 support (2.327.1 or newer).

## Inputs

| Input | Description | Default |
| --- | --- | --- |
| `name` | Name of the artifact | `artifact` |
| `path` | Files, directories, or newline-separated paths to upload | `Required` |
| `if-no-files-found` | Behavior when no files match; warn, error, or ignore | `warn` |
| `retention-days` | Retention in days; zero uses the repository default | `0` |
| `compression-level` | ZIP compression level from zero to nine | `6` |
| `include-hidden-files` | Include hidden files only when explicitly requested | `false` |

## Outputs

| Output | Description |
| --- | --- |
| `artifact-id` | Immutable artifact ID |
| `artifact-url` | Authenticated artifact download URL |
| `artifact-digest` | SHA-256 digest of the uploaded archive |

## Usage

```yaml
- uses: Onemind-Services-LLC/actions/actions/artifact-upload@master
  with:
    name: image-app
    path: |
      ${{ runner.temp }}/image.tar
      ${{ runner.temp }}/image.json
    if-no-files-found: error
    compression-level: 0
    retention-days: 3
```

Uploads always use ZIP archives, including single-file artifacts. Existing names,
paths, and retention settings remain caller-controlled. Hidden files are excluded
by default. Use unique names within a run; this action does not overwrite artifacts.
