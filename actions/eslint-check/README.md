# ESLint Check

Run ESLint and fail on any issue (treats warnings as errors).

## Inputs

- `node-version`: Node.js version (default: `22.x`).
- `working-directory`: Directory to run in (default: `.`).
- `config`: Path to ESLint config file (default: `eslint.config.mjs`). If the file is not found in the working directory, the action runs with ESLint's autodiscovery.
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
      config: 'eslint.config.mjs'
      eslint-args: '.'
```
