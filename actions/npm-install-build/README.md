# NPM Install & Build (Composite Action)

Installs dependencies and builds a Node.js project using npm with caching and optional private registry authentication.

## Inputs

- node-version: Node.js version (default: `22.x`).
- working-directory: Project directory (default: `.`).
- install: Whether to run the install step (default: `true`).
- install-command: Install command (default: `npm ci --no-audit`).
- build: Whether to run the build step (default: `true`).
- build-command: Build command (default: `npm run build`).
- registry-url: npm registry URL for private/scoped packages (optional).
- registry-scope: npm scope for authentication (optional).
- npm-token: npm auth token for private registry access (optional; pass `${{ secrets.NPM_TOKEN }}`).

## Caching

- Uses `actions/setup-node@v4` with `cache: npm` and `cache-dependency-path: <working-directory>/package-lock.json`.

## Usage

```yaml
jobs:
  build:
    runs-on: ubuntu-22.04-sh
    steps:
      - uses: actions/checkout@v5

      - name: Install & Build
        uses: Onemind-Services-LLC/actions/actions/npm-install-build@master
        with:
          node-version: '22'
          working-directory: '.'
          install: true
          # install-command: 'npm ci --prefer-offline'
          build: true
          # build-command: 'npm run build -- --debug'
          # Optional private registry
          # registry-url: 'https://registry.npmjs.org'
          # registry-scope: '@your-scope'
          # npm-token: ${{ secrets.NPM_TOKEN }}

      # Example: install only (skip build)
      - name: Install only
        uses: Onemind-Services-LLC/actions/actions/npm-install-build@master
        with:
          install: true
          build: false
```

## Notes

- This action does not run tests; it only installs and builds.
- For private registries, `actions/setup-node` configures `.npmrc` and `NODE_AUTH_TOKEN` is provided to the npm commands.
- Ensure `package-lock.json` exists for best cache efficiency.
