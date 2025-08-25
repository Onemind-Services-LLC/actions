# Git Diff Check (Composite Action)

Compute changed files between a base and HEAD using git. Supports automatic base resolution for pull requests, optional path filtering, and failing the job when changes are detected.

## Inputs

- working-directory: Directory to run in (default: `.`).
- base-ref: Base ref/commit to compare (default: PR base merge-base or `HEAD~1`).
- head-ref: Head ref/commit (default: `HEAD`).
- fetch-depth: Depth to fetch from origin when discovering base (default: `50`, `0` = full).
- diff-filter: Passed to `git --diff-filter` (default: `ACMR`).
- paths: Newline-delimited pathspecs to filter (optional).
- fail-if-changed: `true` to fail if any files changed (default: `false`).
- compare-working-tree: `true` to diff working tree vs `HEAD` (no commits), default `false`.

## Outputs

- changed: `true` if any files changed after filtering.
- count: Number of changed files.
- files: Newline-delimited list of changed files.
- base: Resolved base ref/commit.
- head: Resolved head ref/commit.

## Behavior

- If `base-ref` is empty and the event is a PR, it fetches `origin/<base>` and uses `merge-base` with the PR base branch.
- Otherwise, it uses `HEAD~1` as base.
- Uses `git diff --name-only` with `--diff-filter` to compute the change list and optional pathspec filters.
  - When `compare-working-tree: true`, diffs working tree changes against `HEAD`.
- Writes a summary section with change details. If `fail-if-changed` is true and changes are found, the step fails.

## Usage

```yaml
steps:
  - uses: actions/checkout@v5

  - id: diff
    uses: Onemind-Services-LLC/actions/actions/git-diff-check@master
    with:
      # base-ref: ''        # auto-resolve
      # head-ref: ''        # defaults to HEAD
      # paths: |
      #   src/**
      #   package.json
      diff-filter: ACMR
      fail-if-changed: 'true'

  - name: Print changed files
    if: steps.diff.outputs.changed == 'true'
    run: |
      echo "Changed files (${{ steps.diff.outputs.count }}):"
      printf '%s\n' "${{ steps.diff.outputs.files }}"
```

Notes:
- Ensure the repository is checked out with sufficient history. This action will `git fetch` when resolving PR bases, controlled by `fetch-depth`.
