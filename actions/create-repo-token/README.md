# Create Repository Token (Composite Action)

Generates a GitHub App installation token using `actions/create-github-app-token` and exposes only the token as an output. Supports scoping to one repo, multiple repos, or all repos in an owner's installation.

## Inputs

- app-id: GitHub App ID. Optional; defaults to `vars.APP_ID`.
- private-key: GitHub App private key (PEM). Optional; defaults to `secrets.APP_PRIVATE_KEY`. Escaped newlines (\\n) are supported.
- owner: Owner of the installation. Optional; defaults to `github.repository_owner` when omitted.
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
        # Pin to a tag or commit SHA in production for supply-chain security
        uses: Onemind-Services-LLC/actions/actions/create-repo-token@master
        id: repo-token

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
          owner: ${{ github.repository_owner }}
```

Alternatively, pass explicit app credentials:

```yaml
      - name: Create token explicitly
        uses: Onemind-Services-LLC/actions/actions/create-repo-token@master
        id: repo-token
        with:
          app-id: ${{ vars.APP_ID }}
          private-key: ${{ secrets.APP_PRIVATE_KEY }}
```

Security tips:
- Do not echo tokens or secrets; this action masks the token in logs.
- Pin third-party actions by version or commit SHA; avoid `@master` in production.
- Grant only minimal permissions in workflows.
