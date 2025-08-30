# ESLint Check

Run ESLint and fail on any issue (treats warnings as errors).

## Inputs

- `node-version`: Node.js version (default: `22.x`).
- `working-directory`: Directory to run in (default: `.`).
- `config`: Path to ESLint config file (default: `eslint.config.mjs`). If the file is not found in the working directory, the action runs with ESLint's autodiscovery.
- `eslint-args`: Additional args/targets (default: `.`).
- `version` (optional): ESLint version or dist-tag to run via `npx` (e.g., `9.9.0` or `latest`). Defaults to the `npx` resolution if omitted.

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
      # version: '9.9.0' # optional
```

Notes:
- This action runs ESLint via `npx` and does not install repository dependencies. If your ESLint config requires plugins/configs that are only present in your repo, either vendor them into the repo or run ESLint from your own workflow with your preferred install strategy.
