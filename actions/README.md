# Composite Actions

Reusable composite GitHub Actions maintained in this repository. Each action includes its own README with inputs, outputs, and examples.

## Available Actions

- NPM Install & Build: Install dependencies and build a Node.js project with npm caching and optional private registry auth. [Docs](npm-install-build/README.md)
- Docker Build, Push, and Sign: Build with Docker Buildx, optionally push, and keyless‑sign Docker images. [Docs](docker-build-push/README.md)
- Cosign Sign: Keyless signing for Docker images or Helm charts using Sigstore Cosign. [Docs](cosign-sign/README.md)
- Create Repository Token: Create a GitHub App installation token scoped to specific repos. [Docs](create-repo-token/README.md)
- Python Setup & Install: Set up Python, optionally upgrade pip, and install from requirements files with optional private auth and extra commands. [Docs](python-setup-install/README.md)
- Django Test Runner: Run Django checks, migrations, collectstatic, tests, and generate coverage XML. [Docs](django-test-runner/README.md)
- Yamllint: Lint YAML files using yamllint with an isolated virtual environment; configurable format and failure mode. [Docs](yamllint/README.md)
- Cypress Test: Run Cypress component or e2e tests with optional server start and wait-on; uploads screenshots on failure. [Docs](cypress-test/README.md)

## Versioning

- Reference actions using a tagged release (e.g., `@v1`) or a commit SHA.
- Avoid `@master` in production workflows.

## Conventions

- Inputs include clear descriptions and sensible defaults.
- Steps are small, composable, and pinned to versions.
- YAML and Markdown use 2‑space indentation.
