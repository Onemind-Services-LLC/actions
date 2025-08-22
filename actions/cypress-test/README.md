# Cypress Test (Composite Action)

Wraps `cypress-io/github-action` to run Cypress component or e2e tests, with optional server start and wait-on. On failure, screenshots are uploaded automatically.

## Inputs

- browser: Browser to run (`chrome`, `edge`, `firefox`). Required.
- component: Run in component test mode (`false` for e2e). Default `true`.
- start: Command to start the app/server for e2e. Optional.
- wait-on: URL(s) to wait for before running tests. Optional.
- wait-on-timeout: Timeout in seconds for waits. Default `300`.

## Usage

### Component Example

```yaml
jobs:
  cypress-component:
    runs-on: ubuntu-22.04-sh
    steps:
      - uses: actions/checkout@v4
      - name: Run unit tests (Cypress component)
        uses: Onemind-Services-LLC/actions/actions/cypress-test@master
        with:
          browser: chrome
          component: true
```

### E2E Example

```yaml
jobs:
  cypress-e2e:
    runs-on: ubuntu-22.04-sh
    steps:
      - uses: actions/checkout@v4
      - name: Run e2e tests
        uses: Onemind-Services-LLC/actions/actions/cypress-test@master
        with:
          browser: firefox
          component: false
          start: npm run local:test
          wait-on: http://localhost:3000
          wait-on-timeout: 300
```

## Notes

- When `browser: firefox`, `FORCE_FIREFOX_CDP=1` is set automatically to enable CDP.
- On failure, screenshots from `cypress/screenshots` upload as `cypress-screenshots-<browser>`.
