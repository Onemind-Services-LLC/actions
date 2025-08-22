# GitHub Actions (Monorepo)

This repository hosts our reusable GitHub assets:

- Actions: Composite actions under `actions/` (usage and docs).
- Workflows: Reusable workflows under `.github/workflows/`.

Start here:

- Actions Overview: [actions/README.md](actions/README.md)
- Workflows Overview: [.github/README.md](.github/README.md)

Notes
- Pin third‑party actions by version/commit; avoid `@master`.
- Keep permissions minimal; add `id-token: write` only when needed.
- Do not print secrets; prefer `GITHUB_TOKEN` where possible.

## YAML Linting

- Composite Action: Yamllint action for linting YAML using an isolated venv. See [actions/yamllint/README.md](actions/yamllint/README.md) for inputs and usage.
- Repo CI: Minimal workflow at `.github/workflows/ci.yml` runs the Yamllint action against this repo using `.yamllint.yaml`.
