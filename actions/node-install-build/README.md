# Node Install & Build (Composite Action)

Installs dependencies and builds a Node.js project using npm, Yarn, pnpm, or npx (build only) with caching and optional private registry authentication.

## Inputs

- package-manager: Package manager to use (`npm`, `yarn`, `pnpm`, or `npx`; default: `npm`).
- node-version: Node.js version (default: `22.x`).
- working-directory: Project directory (default: `.`).
- install: Whether to run the install step (default: `true`).
- install-command: Explicit install command to run (optional; overrides defaults).
- build: Whether to run the build step (default: `true`).
- build-command: Explicit build command to run (optional; overrides defaults).
- registry-url: npm registry URL for private/scoped packages (optional).
- registry-scope: npm scope for authentication (optional).
- npm-token: npm auth token for private registry access (optional; pass `${{ secrets.NPM_TOKEN }}`).

## Defaults per Manager

- npm: `install = npm ci --no-audit`, `build = npm run build`.
- yarn: `install = yarn install --frozen-lockfile`, `build = yarn build`.
- pnpm: `install = pnpm install --frozen-lockfile`, `build = pnpm run build`.
- npx: no default install; `build-command` must be provided (e.g., `npx -y <tool> build`).

## Caching

- Uses `actions/setup-node@v4` with `cache: npm`/`yarn`/`pnpm` and dependency path:
  - npm: `<working-directory>/package-lock.json`
  - yarn: `<working-directory>/yarn.lock`
  - pnpm: `<working-directory>/pnpm-lock.yaml`

## Usage

```yaml
jobs:
  build:
    runs-on: ubuntu-22.04-sh
    steps:
      - uses: actions/checkout@v5

      - name: Install & Build (npm)
        uses: Onemind-Services-LLC/actions/actions/node-install-build@master
        with:
          package-manager: npm
          node-version: '22'
          working-directory: '.'
          install: true
          build: true
          # registry-url: 'https://registry.npmjs.org'
          # registry-scope: '@your-scope'
          # npm-token: ${{ secrets.NPM_TOKEN }}

      - name: Install & Build (Yarn)
        uses: Onemind-Services-LLC/actions/actions/node-install-build@master
        with:
          package-manager: yarn
          install: true
          build: true
          # install-command: 'yarn install --immutable' # for Yarn Berry
      
      - name: Install & Build (pnpm)
        uses: Onemind-Services-LLC/actions/actions/node-install-build@master
        with:
          package-manager: pnpm
          install: true
          build: true

      - name: Build only with npx
        uses: Onemind-Services-LLC/actions/actions/node-install-build@master
        with:
          package-manager: npx
          install: false
          build: true
          build-command: 'npx -y vite build'
```

## Notes

- This action does not run tests; it only installs and builds.
- For private registries, `actions/setup-node` configures auth and `NODE_AUTH_TOKEN` is available to the package manager.
- Ensure the appropriate lockfile exists (`package-lock.json`, `yarn.lock`, or `pnpm-lock.yaml`) for best cache efficiency.
- For Yarn Berry (v2+), consider overriding `install-command` to `yarn install --immutable`.
- For pnpm, Node >= 16 with `corepack` enabled ensures correct pnpm version.
- For npx, you must provide a `build-command` explicitly.
