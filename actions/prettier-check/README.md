# Prettier Check

Run Prettier in check mode with caching over a configurable glob.

## Inputs

- `node-version`: Node.js version (default: `22.x`).
- `working-directory`: Directory to run Prettier in (default: `.`).
- `patterns`: Glob of files to check (default: `**/*.+(js|jsx|ts|tsx|json|css|scss)`).

## Example

```yaml
steps:
  - uses: actions/checkout@v5
  - name: Prettier
    uses: Onemind-Services-LLC/actions/actions/prettier-check@master
    with:
      node-version: '22.x'
      working-directory: '.'
      patterns: '**/*.+(js|jsx|ts|tsx|json|css|scss)'
```
