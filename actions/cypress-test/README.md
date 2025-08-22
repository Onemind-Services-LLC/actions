## Cypress Test (Composite Action)

- Purpose: Wraps `cypress-io/github-action` to run Cypress component or e2e tests, with optional server start and wait-on. On failure, screenshots are uploaded automatically.
- Inputs:
  - `browser` (required): `chrome`, `edge`, or `firefox`.
  - `install` (default `true`): Run install via the Cypress action.
  - `component` (default `true`): `true` for component tests; set to `false` for e2e.
  - `start` (optional): Command to start the app/server for e2e.
  - `wait-on` (optional): URL(s) to wait for before running tests.
  - `wait-on-timeout` (default `300`): Timeout in seconds for waits.

Notes:
- When `browser: firefox`, `FORCE_FIREFOX_CDP=1` is set automatically to enable CDP.
- On failure, screenshots from `cypress/screenshots` are uploaded as an artifact named `cypress-screenshots-${{ inputs.browser }}`.

### Component Example

```yaml
- name: Run unit tests (Cypress component)
  uses: Onemind-Serviecs-LLC/actions/actions/cypress-test@master
  with:
    browser: chrome
    install: true
    component: true
```

### E2E Example

```yaml
- name: Run e2e tests
  uses: Onemind-Serviecs-LLC/actions/actions/cypress-test@master
  with:
    browser: firefox
    component: false
    install: true
    start: npm run local:test
    wait-on: http://localhost:3000
    wait-on-timeout: 300
```
