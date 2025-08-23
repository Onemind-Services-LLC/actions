# ESLint Check

Run ESLint and fail on any issue (treats warnings as errors).

## Inputs

- `node-version`: Node.js version (default: `22.x`).
- `working-directory`: Directory to run in (default: `.`).
- `eslint-args`: Additional args/targets (default: `.`).

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
```

