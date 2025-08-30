# ESLint Check

Run ESLint and fail on any issue (treats warnings as errors).

## Inputs

- `node-version`: Node.js version (default: `22.x`).
- `working-directory`: Directory to run in (default: `.`).
- `config`: Path to ESLint config file (default: `eslint.config.mjs`). If the file is not found in the working directory, the action runs with ESLint's autodiscovery.
- `eslint-args`: Additional args/targets (default: `.`).
- `npm-token` (optional): NPM auth token used when your project depends on private packages (e.g., GitHub Packages). Provide a token if private dependencies are required during install.

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
      # npm-token: ${{ steps.repo-token.outputs.token }} # if private packages are needed
```

Notes:
- If your repository uses private packages (e.g., from GitHub Packages), pass an `npm-token`. In reusable workflows, you can generate a scoped token via the `create-repo-token` action and forward it here.
