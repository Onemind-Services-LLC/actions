# Next.js Bundle Analysis

Reusable workflow to generate Next.js bundle analysis using npm, upload the analysis artifact, compare against the base branch when available, and post/update a PR comment.

## Requirements

- A Next.js app that builds with `npm`.
- No plugin changes required. This uses `nextjs-bundle-analysis` to parse `.next` output after a build.

## Usage

Call the reusable workflow from your repository:

```yaml
name: Bundle Analysis

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  analyze:
    uses: Onemind-Services-LLC/actions/.github/workflows/nextjs-bundle-analyzer.yml@master
    permissions:
      contents: read
      actions: read
      pull-requests: write
    with:
      runner: 'ubuntu-22.04-sh'                   # Optional: defaults to ubuntu-22.04-sh
      node-version: '18'
      working-directory: '.'
      # Optional: custom install command (defaults to npm ci --no-audit)
      # install-command: 'npm ci --prefer-offline'
      # Optional: custom build command (defaults to npm run build)
      # build-command: 'npm run build -- --debug'
      # Optional: provide extra env vars (KEY=VALUE lines)
      extra-env: |
        NEXT_PUBLIC_API_URL=${{ secrets.NEXT_PUBLIC_API_URL }}
    secrets:
      github-token: ${{ secrets.GITHUB_TOKEN }}   # required for artifact download + PR comments
```

Comparison runs automatically using the PR base branch artifact if available.

For monorepos, set `working-directory` to your app subfolder.

### Private/Scoped Registries (optional)

If your repo installs from a private or scoped npm registry, pass the registry URL/scope and map your token to the reusable workflow secret `npm-token`.

```yaml
jobs:
  analyze:
    uses: Onemind-Services-LLC/actions/.github/workflows/nextjs-bundle-analyzer.yml@master
    with:
      registry-url: 'https://registry.npmjs.org'  # or your private registry
      registry-scope: '@your-scope'               # optional
    secrets:
      github-token: ${{ secrets.GITHUB_TOKEN }}   # map caller's GitHub token
      npm-token: ${{ secrets.NPM_TOKEN }}         # map caller's secret to reusable workflow
```

## Inputs

- node-version: Node.js version (default: `18`).
- runner: GitHub runner label (default: `ubuntu-22.04-sh`).
- working-directory: Directory of the Next.js app (default: `.`).
- install-command: Custom install command; overrides defaults.
- build-command: Custom build command; overrides defaults.
- extra-env: Newline `KEY=VALUE` pairs exported to job env via GITHUB_ENV.
- Artifact name and path are fixed: `next-bundle-analysis` and `.next/analyze/__bundle_analysis.json`.
- registry-url: npm registry URL for private/scoped packages (optional).
- registry-scope: npm scope for authentication (optional).
  - Provide `secrets.npm-token` when using a private registry.
  - Provide `secrets.github-token` for artifact download and PR comments.

## Notes

- On forks, `pull_request` workflows may lack permission to comment; analysis and artifacts still upload.
- If you prefer `pull_request_target`, review security implications before enabling.
- The workflow uses ephemeral `npx -y nextjs-bundle-analysis`; no dependency needs to be added to your app.
- For private registries, `actions/setup-node` configures `.npmrc` and uses `NODE_AUTH_TOKEN` during install when `registry-url` is set. Provide `secrets.npm-token` in the call (map from your repo/org secret).
- Extra env vars are provided via `extra-env` as newline `KEY=VALUE` pairs and applied using the GITHUB_ENV mechanism.
