# Yamllint

Lint YAML files using yamllint with a self-contained virtual environment. Suitable for reuse across repositories and in this repo's CI.

## Inputs

- `config_file` (optional): Path to yamllint configuration. Default: `.yamllint.yaml`.
- `file_or_dir` (optional): File or directory to lint (space-separated allowed). Default: `.`
- `format` (optional): Output format (`standard`, `parsable`, `github`, `colored`, `auto`). Default: `github`.
- `fail-on-warnings` (optional): Treat warnings as failures. Default: `false`.

## Usage

```yaml
jobs:
  lint:
    runs-on: ubuntu-22.04-sh
    steps:
      - uses: actions/checkout@v5
      - name: Yamllint
        uses: Onemind-Services-LLC/actions/actions/yamllint@master
        with:
          config_file: .yamllint.yaml
          file_or_dir: .
          format: github
          fail-on-warnings: 'false'
```

