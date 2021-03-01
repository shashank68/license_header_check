# License header checker for python files

A pre-commit hook that checks for license header(copyright year) of python files and updates if required.

This precommit hook checks and inserts license header for .py files.

* Updates copyright year to latest for files to be committed.
* With `--all-files` option, the copyright year is updated only if the file has been modified in the current year.
* Uses `git log` to get the latest modification date
* Inserts header if not already present.

## Usage

Add the below config to `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/shashank68/license_header_check/
    rev: "1.1"
    hooks:
    -   id: license-header-check
        name: License header check
        files: \.py$
```

## Manual Run

```bash
    pre-commit run license-header-check [--all-files]
```
