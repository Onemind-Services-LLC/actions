# Repository Guidelines

This document outlines how to work in this monorepo of reusable GitHub Actions and workflows. For detailed catalogs:

- Actions Overview: `actions/README.md`
- Workflows Overview: `.github/README.md`

## Project Structure & Module Organization

- `actions/`: Composite actions (each directory contains an action + README). See `actions/README.md` for the full list.
- `.github/workflows/`: Reusable workflows (e.g., `docker-build-push.yml`, `netbox-plugin-tests.yml`, `pre-commit.yml`). See `.github/README.md`.
- `.github/pull_request_template.md`: Required PR checklist and Jira link format.
- `README.md`: High-level usage and entry points to module docs.

## Build, Test, and Development Commands

- No build step; this repo ships YAML and composite actions.
- Validate YAML locally: `yamllint .` (recommended) or open in VS Code with YAML schema support.
- Dry-run workflows with `act` (optional):
  - `act -W .github/workflows/pre-commit.yml -j pre-commit`
  - `act -W .github/workflows/netbox-plugin-tests.yml -j test` (requires Docker services)
  - `act -W .github/workflows/docker-build-push.yml -j build` (requires Docker Buildx)
- Best practice: consume the actions/workflows from a sandbox repo and open a PR to verify end-to-end.

## Coding Style & Naming Conventions

- Indentation: 2 spaces in YAML and Markdown; no tabs.
- Filenames: kebab-case for workflows and action folders (e.g., `pre-commit.yml`).
- Workflow/job/step names: Title Case, clear and action-oriented.
- Keep inputs descriptive with `description` and sensible `default` values.
- Prefer small, composable steps; avoid shell one-liners that hide errors.

## Testing Guidelines

- This repo has no unit tests; validate by running the reusable workflows or consuming the composite actions in a sandbox repo.
- For `netbox-plugin-tests.yml`, the workflow provides a baseline NetBox test configuration; pass plugin settings via the `plugin-configuration` input as an inner plugin config JSON string only (e.g., `'{"github_token":"ghp_xxx"}'`). The workflow wraps this under the plugin name and writes a valid Python `PLUGINS_CONFIG = {'<plugin-name>': {...}}` preserving quotes. Ensure your plugin supports the selected NetBox version and works with Redis/Postgres services.
- Use matrix or sample invocations in a test repo before changing defaults.
- Verify documentation examples by copy-pasting into a scratch workflow.

## Commit & Pull Request Guidelines

- Reference Jira when applicable: `OMS-1234 short, present-tense summary`.
- Use `[skip ci]` for docs-only changes if no validation is needed.
- Open PRs with:
  - Clear description, linked Jira, and scope of change.
  - Notes on backwards compatibility and any required secrets/permissions (e.g., `vars.APP_ID`, `secrets.APP_PRIVATE_KEY` for NetBox plugin tests).
  - Screenshots or logs for behavior changes.
  - Keep diffs small and update module READMEs when inputs/behavior change.

## Security & Configuration Tips

- Do not print secrets; prefer `GITHUB_TOKEN` when possible. For NetBox plugin tests, provide GitHub App credentials (`vars.APP_ID`, `secrets.APP_PRIVATE_KEY`) to mint a short‑lived installation token.
- Use `@master` in examples for actions/workflows from this repo unless an action specifically calls out pinning.
- Third‑party actions/workflows must always be pinned to a version tag or commit SHA (no floating refs like `@master`).
- Limit permissions to the minimum needed in workflows.
