# Browserslist Lock Check

Run `update-browserslist-db` and fail if it modifies `package-lock.json` or `yarn.lock`.

## Inputs

- `node-version`: Node.js version (default: `22.x`).
- `working-directory`: Directory to run in (default: `.`).
- `update-command`: Update command (default: `npx --yes update-browserslist-db@latest`).

## Example

```yaml
steps:
  - uses: actions/checkout@v5
  - name: Browserslist Lock Check
    uses: Onemind-Services-LLC/actions/actions/browserslist-lock-check@master
    with:
      node-version: '22.x'
      working-directory: '.'
      update-command: "npx --yes update-browserslist-db@latest"
```

