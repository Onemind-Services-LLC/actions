# GitHub Actions (Monorepo)

This repository hosts our reusable GitHub assets:

- Actions: Composite actions under `actions/` (usage and docs).
- Workflows: Reusable workflows under `.github/workflows/`.

Start here:

- Actions Overview: [actions/README.md](actions/README.md)
- Workflows Overview: [.github/README.md](.github/README.md)
- Best Practices: [BEST_PRACTICES.md](BEST_PRACTICES.md)

Pinning: Use `@master` in examples unless an action explicitly requires a tag or SHA.

Notes
- Use `@master` for actions/workflows from this repo in examples unless otherwise specified.
- Third-party actions/workflows must always be pinned to a version tag or commit SHA (do not use floating refs like `@master`).
- Keep permissions minimal; add `id-token: write` only when needed.
- Do not print secrets; prefer `GITHUB_TOKEN` where possible.

## YAML Linting

- Composite Action: Yamllint action for linting YAML using an isolated venv. See [actions/yamllint/README.md](actions/yamllint/README.md) for inputs and usage.
- Repo CI: Minimal workflow at `.github/workflows/ci.yml` runs the Yamllint action against this repo using `.yamllint.yaml`.

## Build, Test, and Development

- Validate YAML locally: `yamllint .` (recommended) or open in VS Code with YAML schema support.
- Optional local dry-runs with `act`:
  - `act -W .github/workflows/pre-commit.yml -j pre-commit`
  - `act -W .github/workflows/netbox-plugin-tests.yml -j test`
  - `act -W .github/workflows/docker-build-push.yml -j build`
- Best practice: consume actions/workflows from a sandbox repo and open a PR to verify end-to-end.

## Style & Conventions

- Indentation: 2 spaces in YAML and Markdown; no tabs.
- Filenames: kebab-case for workflows and action folders (e.g., `pre-commit.yml`).
- Workflow/job/step names: Title Case, clear and action-oriented.
- Keep inputs descriptive with `description` and sensible defaults.
- Prefer small, composable steps; avoid shell one-liners that hide errors.

## Testing Guidelines

- This repo has no unit tests; validate by running reusable workflows or consuming composite actions in a sandbox repo.
- For `netbox-plugin-tests.yml`, pass plugin settings via the `plugin-configuration` input as an inner JSON string only (e.g., `'{"github_token":"ghp_xxx"}'`). The workflow wraps this under the plugin name and writes a valid Python `PLUGINS_CONFIG = {'<plugin-name>': {...}}` preserving quotes.
- Ensure your plugin supports the selected NetBox version and works with Redis/Postgres services.
- Use a matrix or sample invocations in a test repo before changing defaults.

## Commit & PR Guidelines

- Reference Jira when applicable: `OMS-1234 short, present-tense summary`.
- Use `[skip ci]` for docs-only changes if no validation is needed.
- Open PRs with:
  - Clear description, linked Jira, and scope of change.
  - Notes on backwards compatibility and any required secrets/permissions (e.g., `vars.APP_ID`, `secrets.APP_PRIVATE_KEY`).
  - Screenshots or logs for behavior changes.
  - Keep diffs small and update module READMEs when inputs/behavior change.

## Security & Configuration

- Do not print secrets; prefer `GITHUB_TOKEN` when possible.
- Use `@master` in examples for this repo’s actions/workflows; third-party actions/workflows must be pinned by tag or commit SHA.
- Limit permissions to the minimum needed in workflows.
