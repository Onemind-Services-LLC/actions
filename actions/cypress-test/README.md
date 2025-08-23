# Cypress Test (Composite Action)

Wraps `cypress-io/github-action` to run Cypress component or e2e tests, with optional server start and wait-on. On failure, screenshots are uploaded automatically.

## Inputs

- node-version: Node.js version to use (default: `22.x`).
- working-directory: Project directory (default: `.`).
- registry-url: npm registry URL for private/scoped packages (optional).
- registry-scope: npm scope for auth, e.g., `@your-scope` (optional).
- npm-token: npm auth token for private registry access (optional).
- browser: Browser to run (`chrome`, `chrome-for-testing`, `edge`, `firefox`). Required.
- component: Run in component test mode (`false` for e2e). Default `true`.
- start: Command to start the app/server for e2e (optional).
- wait-on: URL(s) to wait for before running tests (optional).
- wait-on-timeout: Timeout in seconds for waits (default: `300`).

## Usage

### Component tests

```yaml
jobs:
  cypress-component:
    runs-on: ubuntu-22.04-sh
    steps:
      - uses: actions/checkout@v5
      - name: Run unit tests (Cypress component)
        uses: Onemind-Services-LLC/actions/actions/cypress-test@master
        with:
          browser: chrome
          component: true
```

### E2E tests with server + wait-on

```yaml
jobs:
  cypress-e2e:
    runs-on: ubuntu-22.04-sh
    steps:
      - uses: actions/checkout@v5
      - name: Run e2e tests
        uses: Onemind-Services-LLC/actions/actions/cypress-test@master
        with:
          browser: firefox
          component: false
          start: npm run local:test
          wait-on: http://localhost:3000
          wait-on-timeout: 300
```

### Private npm registry (optional)

```yaml
jobs:
  cypress-e2e-private:
    runs-on: ubuntu-22.04-sh
    steps:
      - uses: actions/checkout@v5
      - name: Run Cypress with private deps
        uses: Onemind-Services-LLC/actions/actions/cypress-test@master
        with:
          browser: chrome
          # Optional registry auth
          registry-url: https://registry.npmjs.org
          registry-scope: '@your-scope'
          npm-token: ${{ secrets.NPM_TOKEN }}
```

## Notes

- Uses pinned `cypress-io/github-action` to run tests; it installs dependencies in the working directory.
- When `browser: chrome` is provided, this action installs Chrome for Testing and runs Cypress with `chrome-for-testing` under the hood, matching Cypress 14+ detection.
- When `browser: firefox`, `FORCE_FIREFOX_CDP=1` is set automatically to enable CDP.
- On failure, screenshots from `cypress/screenshots` are uploaded as `cypress-screenshots-<browser>`.
