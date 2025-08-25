# Detect Package Manager (Composite Action)

Detects the Node.js package manager based on lockfiles in a directory.
Order of precedence: pnpm > yarn > npm. If no lockfile is found, it returns a configurable fallback.

## Inputs

- working-directory: Directory to scan (default: `.`).
- fallback: Fallback when no lockfile is found (`npm`|`yarn`|`pnpm`|`npx`; default: `npm`).

## Outputs

- package-manager: Detected manager (`npm`|`yarn`|`pnpm`|`npx`).
- source: What matched (`pnpm-lock.yaml`|`yarn.lock`|`package-lock.json`|`fallback`).
- lockfile: Path to detected lockfile (empty if none).

## Usage

```yaml
steps:
  - uses: actions/checkout@v5

  - id: pm
    name: Detect Package Manager
    uses: Onemind-Services-LLC/actions/actions/detect-package-manager@master
    with:
      working-directory: '.'
      # fallback: npm

  - name: Setup Node
    uses: Onemind-Services-LLC/actions/actions/node-install-build@master
    with:
      package-manager: ${{ steps.pm.outputs.package-manager }}
      node-version: '22.x'
      install: true
      build: false
```

Notes:
- Fallback allows `npx`, which has no lockfile; use when you only run build tools via `npx` and don’t install dependencies.
