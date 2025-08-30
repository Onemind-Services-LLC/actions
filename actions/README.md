# Composite Actions

Reusable composite GitHub Actions maintained in this repository. Each action includes its own README with inputs, outputs, and examples.

## Available Actions

- Node Install & Build: Install dependencies and build a Node.js project using npm, Yarn, pnpm, or npx (build only) with caching and optional private registry auth. [Docs](node-install-build/README.md)
- Detect Package Manager: Detect npm/yarn/pnpm from lockfiles with a fallback output. [Docs](detect-package-manager/README.md)
- Git Diff Check: Compute changed files between refs using git, with filtering and optional failure. [Docs](git-diff-check/README.md)
- Code Coverage Summary: Generate coverage summary (Cobertura XML) and post a sticky PR comment. [Docs](cobertura-report/README.md)
- NPM Install & Build: Install dependencies and build a Node.js project with npm caching and optional private registry auth. [Docs](npm-install-build/README.md)
- Docker Build, Push, and Sign: Build with Docker Buildx, optionally push, and keyless‑sign Docker images. [Docs](docker-build-push/README.md)
- Cosign Sign: Keyless signing for Docker images or Helm charts using Sigstore Cosign. [Docs](cosign-sign/README.md)
- Create Repository Token: Create a GitHub App installation token scoped to specific repos. [Docs](create-repo-token/README.md)
- Python Setup & Install: Set up Python, optionally upgrade pip, and install from requirements files with optional private auth and extra commands. [Docs](python-setup-install/README.md)
- Django Test Runner: Run Django checks, migrations, collectstatic, tests, and generate coverage XML. [Docs](django-test-runner/README.md)
- Python Library Tests: Run mypy and pytest with coverage for Python libraries; optional coverage PR comment. [Docs](python-library-tests/README.md)
- Yamllint: Lint YAML files using yamllint (installed via pip); configurable format and failure mode. [Docs](yamllint/README.md)
- Cypress Test: Run Cypress component or e2e tests with optional server start and wait-on; uploads screenshots on failure. [Docs](cypress-test/README.md)
- Prettier Check: Run Prettier in check mode with caching over a glob. [Docs](prettier-check/README.md)
- ESLint Check: Run ESLint and fail on any issue. [Docs](eslint-check/README.md)
- Browserslist Lock Check: Ensure updating Browserslist DB does not modify lockfiles. [Docs](browserslist-lock-check/README.md)
- yq - Portable YAML Processor: Run pinned `mikefarah/yq` in Docker to create, read, update, delete, merge, and validate YAML. [Docs](yq/README.md)
- TypeScript Type Check: Run TypeScript compiler in type-check mode (`--noEmit`) with auto PM detection. [Docs](typescript-check/README.md)
- Bundle Integrity Check: Re-run bundling and fail if `dist` changes to enforce deterministic artifacts. [Docs](bundle-integrity-check/README.md)

## Versioning

- Use `@master` in examples by default.
- If an action specifically requires pinning, its README will call out using a tag or commit SHA.

Third‑party actions/workflows: In all examples and consumer workflows, third‑party actions must be pinned to a version tag or commit SHA; do not use floating refs like `@master`.

## Conventions

- Inputs include clear descriptions and sensible defaults.
- Steps are small, composable, and pinned to versions.
- YAML and Markdown use 2‑space indentation.
