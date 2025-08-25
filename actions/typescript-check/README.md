# TypeScript Type Check (Composite Action)

Runs the TypeScript compiler in type-check mode (no emit) with auto detection of the project's package manager and optional dependency install.

## Inputs

- node-version: Node.js version (default: `22.x`).
- working-directory: Directory to run in (default: `.`).
- install: Whether to install dependencies first (default: `true`).
- install-command: Explicit install command (optional).
- tsconfig: Path to `tsconfig.json` (optional; auto-detected when empty).
- tsc-args: Additional args for `tsc` (default: `--noEmit`).

## Behavior

- Detects npm/yarn/pnpm via lockfiles and uses the unified `node-install-build` action.
- Runs `npx tsc` with `--noEmit` by default; supports `-p <tsconfig>` selection.

## Usage

```yaml
steps:
  - uses: actions/checkout@v5

  - name: TypeScript Type Check
    uses: Onemind-Services-LLC/actions/actions/typescript-check@master
    with:
      node-version: '22.x'
      working-directory: '.'
      install: 'true'
      # tsconfig: 'tsconfig.json'
      # tsc-args: '--noEmit --pretty'
```

Notes:
- Ensure `typescript` is available (as a local devDependency or via `npx` on-demand resolution).
