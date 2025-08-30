# ESLint Check

Run ESLint and fail on any issue (treats warnings as errors). The action executes ESLint via `npx -p eslint@<version> eslint` for an ephemeral, pinned installation and invokes `eslint` with `--max-warnings=0`.

## Inputs

- `node-version`: Node.js version (default: `22.x`).
- `working-directory`: Directory to run in (default: `.`).
- `eslint-args`: Additional args/targets (default: `.`).
- `version` (optional): ESLint package version or dist-tag to run via `npx -p` (e.g., `9.9.0` or `latest`). If omitted, `npx` resolves the default dist-tag.

## Example

```yaml
steps:
  - uses: actions/checkout@v5
  - name: ESLint
    uses: Onemind-Services-LLC/actions/actions/eslint-check@master
    with:
      node-version: '22.x'
      working-directory: '.'
      eslint-args: '.'
      # Pin ESLint (optional). Without this, the default dist-tag is used.
      # version: '9.9.0'
```
