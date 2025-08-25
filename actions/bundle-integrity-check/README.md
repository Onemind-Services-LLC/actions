# Bundle Integrity Check (Composite Action)

Re-run your bundling step and fail if committed dist artifacts change. This enforces deterministic bundles and ensures dist files are up to date and committed.

## Inputs

- node-version: Node.js version (default: `22.x`).
- working-directory: Directory to run the bundler in (default: `.`).
- dist-path: Repo-relative path to bundled output (default: `<working-directory>/dist`).
- install: Install dependencies before bundling (default: `true`).
- install-command: Custom install command (optional).
- bundle-command: Custom bundle command (optional). If omitted, defaults by PM:
  - npm: `npm run bundle`
  - yarn: `yarn bundle`
  - pnpm: `pnpm run bundle`

## Behavior

- Detects npm/yarn/pnpm via lockfiles under `working-directory`.
- Sets up Node and optionally installs dependencies.
- Runs the bundle command.
- Uses `git-diff-check` to compare the working tree against `HEAD` for the `dist-path`. Fails if any changes are detected.

## Usage

```yaml
steps:
  - uses: actions/checkout@v5

  - name: Bundle Integrity Check
    uses: Onemind-Services-LLC/actions/actions/bundle-integrity-check@master
    with:
      working-directory: netbox_secrets/project-static
      dist-path: netbox_secrets/project-static/dist
      # bundle-command: 'yarn bundle'  # optional override
```

Notes:
- For monorepos, point `working-directory` at the package/app root and set `dist-path` accordingly.
- If your project uses a different script name than `bundle`, set `bundle-command` to that script (e.g., `npm run build`).
