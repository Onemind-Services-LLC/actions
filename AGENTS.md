# Repository Guidelines

## Project Structure & Module Organization

- `.github/workflows/`: Reusable workflows (`netbox-plugin-tests.yml`, `pre-commit.yml`).
- `netbox-plugin-testing/`: Composite action wrapper + docs for NetBox plugin tests.
- `pre-commit-checks/`: Composite action wrapper + docs for pre-commit.
- `.github/pull_request_template.md`: Required PR checklist and Jira link format.
- `README.md`: High-level usage and links to module docs.

## Build, Test, and Development Commands

- No build step; this repo ships YAML and composite actions.
- Validate YAML locally: `yamllint .` (recommended) or open in VS Code with YAML schema support.
- Dry-run workflows with `act` (optional):
  - `act -W .github/workflows/pre-commit.yml -j pre-commit`
  - `act -W .github/workflows/netbox-plugin-tests.yml -j test` (requires Docker services)
- Best practice: consume the workflows from a sandbox repo and open a PR to verify end-to-end.

## Coding Style & Naming Conventions

- Indentation: 2 spaces in YAML and Markdown; no tabs.
- Filenames: kebab-case for workflows and action folders (e.g., `pre-commit.yml`).
- Workflow/job/step names: Title Case, clear and action-oriented.
- Keep inputs descriptive with `description` and sensible `default` values.
- Prefer small, composable steps; avoid shell one-liners that hide errors.

## Testing Guidelines

- This repo has no unit tests; validation happens by running the reusable workflows.
- For `netbox-plugin-tests.yml`, ensure a plugin repo provides `testing_configuration/configuration.py` and matches the required services.
- Use matrix or sample invocations in a test repo before changing defaults.
- Verify documentation examples by copy-pasting into a scratch workflow.

## Commit & Pull Request Guidelines

- Reference Jira when applicable: `OMS-1234 short, present-tense summary`.
- Use `[skip ci]` for docs-only changes if no validation is needed.
- Open PRs with:
  - Clear description, linked Jira, and scope of change.
  - Notes on backwards compatibility and any required secrets/permissions (`secrets.git-token`).
  - Screenshots or logs for behavior changes.
- Keep diffs small and update module READMEs when inputs/behavior change.

## Security & Configuration Tips

- Do not print secrets; prefer `GITHUB_TOKEN` when possible. `netbox-plugin-tests` requires `secrets.git-token` for private deps.
- Pin third-party actions by version/commit; avoid `@master` in new additions.
- Limit permissions to the minimum needed in workflows.
