# Create Repository Token (Composite Action)

Generates a GitHub App installation token using `actions/create-github-app-token` and exposes only the token as an output. Supports scoping to one repo, multiple repos, or all repos in an owner's installation.

Optionally, if a caller already has a suitable token, pass it via `github-token` and this action will skip creation and return the provided token unchanged.

## Inputs

- app-id: GitHub App ID.
- private-key: GitHub App private key (PEM).
- github-token: Optional; if provided, token creation is skipped and this token is returned as the output.
- owner: Owner of the installation. Optional; when `repositories` is provided and `owner` is omitted, defaults to `github.repository_owner`. When both `owner` and `repositories` are omitted, the token is scoped to only the current repository.
- repositories: Comma or newline-separated list of repositories. Optional.
  - If `owner` is set and `repositories` is empty, the token is scoped to all repositories in the owner's installation.
  - If both `owner` and `repositories` are empty, the token is scoped to only the current repository.
- skip-token-revoke: Optional; do not revoke token after job completion when `true`.

## Outputs

- token: GitHub App installation access token.

## Usage

```yaml
name: Run tests on staging
on:
  push:
    branches: [ main ]

jobs:
  hello-world:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Create token for current repo (implicit defaults)
        uses: Onemind-Services-LLC/actions/actions/create-repo-token@master
        id: repo-token
        with:
          app-id: ${{ vars.APP_ID }}
          private-key: ${{ secrets.APP_PRIVATE_KEY }}

      - name: Use token without printing it
        env:
          GH_TOKEN: ${{ steps.repo-token.outputs.token }}
        run: |
          # Example: call GitHub API without exposing the token
          gh api /rate_limit > /dev/null
```

Create a token for multiple repositories in the current owner's installation:

```yaml
      - name: Create token for multiple repos
        uses: Onemind-Services-LLC/actions/actions/create-repo-token@master
        id: repo-token
        with:
          app-id: ${{ vars.APP_ID }}
          private-key: ${{ secrets.APP_PRIVATE_KEY }}
          owner: ${{ github.repository_owner }}
          repositories: |
            repo1
            repo2
```

Create a token for all repositories in the current owner's installation:

```yaml
      - name: Create token for all repos in owner
        uses: Onemind-Services-LLC/actions/actions/create-repo-token@master
        id: repo-token
        with:
          app-id: ${{ vars.APP_ID }}
          private-key: ${{ secrets.APP_PRIVATE_KEY }}
          owner: ${{ github.repository_owner }}
```

Use a pre-existing token from the caller workflow instead of creating a new one:

```yaml
      - name: Reuse an existing token
        uses: Onemind-Services-LLC/actions/actions/create-repo-token@master
        id: repo-token
        with:
          # For example, pass a PAT or a different installation token
          github-token: ${{ secrets.MY_EXISTING_TOKEN }}
          # The following inputs are ignored when github-token is provided
          app-id: ${{ vars.APP_ID }}
          private-key: ${{ secrets.APP_PRIVATE_KEY }}
```

Security tips:
- Do not echo tokens or secrets; this action masks the token in logs.
- Third‑party actions in your workflows must be pinned to a version tag or commit SHA (no floating refs like `@master`).
- Grant only minimal permissions in workflows.
