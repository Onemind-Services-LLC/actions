# Code Coverage Summary (Composite Action)

Generates a Markdown code coverage summary from Cobertura XML using the pinned `irongut/CodeCoverageSummary` action, and posts a sticky pull request comment via the pinned `marocchino/sticky-pull-request-comment` action.

## Inputs

- path: Path/glob to coverage XML (default: `coverage.xml`).
- working-directory: Optional directory to resolve the `path` from (default: `.`; when `.` the `path` is used as-is).
- minimum-coverage: Minimum coverage percentage threshold (default: `80`).
- fail-below-threshold: Fail when below minimum coverage using `thresholds` lower bound (default: `true`).
- show-branch: Show Branch Rate metrics when `true` (maps to `hide_branch_rate: false`).
- report-name: Unique name for the report/comment; used as the sticky comment header (default: `Code Coverage Summary`).
- pull-request-number: Use when not on a `pull_request` trigger (default: empty).
- github-token: Token used to create/update the PR comment. Defaults to the workflow's `${{ github.token }}` when not provided.

## Usage

```yaml
steps:
  - uses: actions/checkout@v5
  - name: Generate coverage
    run: |
      coverage run -m pytest
      coverage xml -o coverage.xml

  - name: Code Coverage Summary
    uses: Onemind-Services-LLC/actions/actions/cobertura-report@master
    with:
      path: 'coverage.xml'
      minimum-coverage: '85'
      fail-below-threshold: 'true'
      # Optional: customize sticky comment header
      report-name: 'My Coverage Summary'
```

Notes:
- Requires job permissions `pull-requests: write` to post PR comments.
- Uses `only_update: true` so it only updates an existing sticky comment; it will not create a new one if none exists.
- Provide `github-token` if commenting across repos or using a GitHub App token; otherwise it falls back to `${{ github.token }}`.
- This is a thin wrapper that keeps the prior interface but now uses `irongut/CodeCoverageSummary` for generation and `marocchino/sticky-pull-request-comment` for commenting.
