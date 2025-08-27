# Best Practices

Practical guidance for using the actions and reusable workflows in this repo safely and effectively.

## Pinning & References

- Internal (this repo): Use `@master` in examples for actions and reusable workflows unless a specific action calls out pinning to a tag or SHA.
- Third‑party: Always pin third‑party actions/workflows to a version tag or commit SHA; avoid floating refs like `@master`.

## Permissions & Security

- Least privilege: Declare only the permissions a job needs (e.g., `contents: read`). Add `id-token: write` only when required (e.g., OIDC signing).
- Secrets hygiene: Never echo secrets. Pass via `secrets.*` or masked env vars, and prefer short‑lived tokens.
- GitHub App tokens: Prefer GitHub App auth over PATs. Use `actions/create-repo-token@master` from this repo to mint installation tokens scoped to specific repos.
- Logs: Avoid printing sensitive configuration (e.g., plugin configs, tokens). Use summaries or artifacts for non‑sensitive outputs.

## Caching & Performance

- Node: Use `actions/setup-node@v4` caching tied to lockfiles. Ensure the correct lockfile exists for npm/yarn/pnpm.
- Python: Use `actions/setup-python@v5` with pip caching; keep `requirements*.txt` up‑to‑date. Separate installs from tests when helpful for cache efficiency.
- Layered steps: Keep install/build/test as separate steps to improve cache reuse and failure visibility.

## Deterministic Builds

- Bundle integrity: Use `actions/bundle-integrity-check@master` to ensure committed `dist` assets are reproducible and up‑to‑date.
- Browserslist database: Use `actions/browserslist-lock-check@master` so DB updates don’t mutate lockfiles.

## Docker Images

- Buildx + metadata: Use `docker/metadata-action` to generate OCI tags/labels and keep annotations consistent.
- Registry cache: Log in even for build‑only to enable registry cache. Use a dedicated `cache-image` per branch.
- SBOM/provenance: Let Buildx generate SBOM and provenance when pushing images. Use OIDC (`id-token: write`) for keyless signing.
- Secrets: Prefer Buildx `secrets` over `build-args` for sensitive values. Never embed secrets into image labels/annotations.

## NetBox Plugin Tests

- Inputs: Provide `plugin-configuration` as an inner JSON string only, wrapped in YAML single quotes. Example: `'{"enabled": true}'`.
- Services: Ensure your plugin supports the selected NetBox version and works with Redis/Postgres.
- Coverage: Limit coverage to the plugin package to exclude NetBox itself.

## Cypress Tests

- Browser matrix: For reusable workflows, pass browsers as a JSON array string (e.g., `'["chrome","edge","firefox"]'`).
- Component vs e2e: Use `component: true` for component tests; set `start` and `wait-on` for e2e.
- Private npm: Use GitHub App credentials to mint a token for scoped private registry access.

## Python Testing

- Types + tests: Run mypy and pytest with coverage via `actions/python-library-tests@master`.
- Coverage focus: Use `coverage-source` or equivalent to scope measurement to your package.
- Editable installs: Install your package in editable mode when appropriate for library testing.

## Workflow Design

- Reuse first: Prefer reusable workflows in `.github/workflows/` to standardize CI across repos.
- Job size: Keep jobs focused and steps small; name steps clearly for better logs.
- Matrices: Use `strategy.matrix` for version/browser/platform coverage. Set `fail-fast: false` when you want independent failures.
- Concurrency: Use `concurrency` with `cancel-in-progress: true` for PR workflows to avoid redundant runs.
- Timeouts: Set `timeout-minutes` on long‑running jobs and steps to fail fast on stuck builds.
- Artifacts: Upload only what you need; set `retention-days` appropriately.

## YAML Quality

- Formatting: Use 2‑space indentation, no tabs. Keep names Title Case and action‑oriented.
- Linting: Run `yamllint` locally or via `actions/yamllint@master` with a shared config.
- Avoid one‑liners: Prefer explicit multi‑line shell scripts for readability and error handling.

## Local Development

- Lint: Run `yamllint .` before pushing changes.
- Dry‑run: Use `act` to exercise workflows locally when practical. Some jobs relying on Docker or OIDC may need adjustments locally.

## Common Pitfalls

- Quoting JSON in YAML: Wrap JSON strings in single quotes and keep inner quotes as double quotes to avoid YAML parsing issues.
- Deprecated output syntax: Write outputs to `$GITHUB_OUTPUT` instead of using deprecated `set-output`.
- Floating refs: Never use floating refs for third‑party actions (must pin to tags/SHAs).

