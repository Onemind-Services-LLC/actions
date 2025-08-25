# Cobertura Report (Composite Action)

Posts a Cobertura coverage report comment on pull requests using the pinned `5monkeys/cobertura-action`.

## Inputs

- path: Path/glob to coverage XML (default: `coverage.xml`).
- repo-token: Token for reporter (optional; often `${{ secrets.GITHUB_TOKEN }}` or an app token).
- skip-covered: Skip files with 100% coverage (default: `true`).
- minimum-coverage: Minimum coverage percentage threshold (default: `80`).
- fail-below-threshold: Fail when below minimum coverage (default: `true`).
- show-line: Show line coverage column (default: `true`).
- show-branch: Show branch coverage column (default: `true`).
- show-class-names: Show class names (default: `false`).
- show-missing: Show missing lines (default: `true`).
- only-changed-files: Only show changed files (default: `false`).
- report-name: Unique name for the report/comment (default: empty).
- pull-request-number: Use when not on a `pull_request` trigger (default: empty).

## Usage

```yaml
steps:
  - uses: actions/checkout@v5
  - name: Generate coverage
    run: |
      coverage run -m pytest
      coverage xml -o coverage.xml

  - name: Cobertura Report
    uses: Onemind-Services-LLC/actions/actions/cobertura-report@master
    with:
      path: 'coverage.xml'
      repo-token: ${{ secrets.GITHUB_TOKEN }}
      minimum-coverage: '85'
      fail-below-threshold: 'true'
```

Notes:
- This is a thin wrapper that keeps a stable interface and pin for `5monkeys/cobertura-action`.
