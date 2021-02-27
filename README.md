# License header checker for python files

A pre-commit hook that checks for license header(copyright year) of python files and updates if required.

## Usage

Add the below config to `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/shashank68/license_header_check/
    rev: "1.0"
    hooks:
    -   id: license-header-check
        name: License header check
        files: \.py$
```

## Manual Run

```bash
    pre-commit run license-header-check [--all-files]
```