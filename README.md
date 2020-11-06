# prose

Initialize projects from predefined templates which support flake8, black, mypy and others.

# Templates

``prose`` delivers templates that are designed to increase the productivity.

## Packages

### Modern Python

Tools required to use the template:

* `git`,
* [`nox`](https://nox.thea.codes/en/stable/),
* [`poetry`](https://python-poetry.org/),
* [`pre-commit`](https://pre-commit.com/),
* [`pyenv`](https://github.com/pyenv/pyenv).


After meeting the requirements, we can initialize a sample project.

```bash
prose --project_name example_prose_package \
    --project_type package \
    --template_name modern_python \
    --python_version 3.8.2
```

Benefits:

* pre-configured `flake8` (with extensions), see:
    ```
    [flake8]
    select = ANN,B,B9,BLK,C,D,DAR,E,F,I,S,W
    ignore = ANN101,E203,E501,W503
    max-line-length = 80
    max-complexity = 10
    application-import-names = ${project_name},tests
    import-order-style = google
    docstring-convention = google
    per-file-ignores = tests/*:S101

    ```
* pre-configured ``pre-commit``, see:
    ```
    repos:
    -   repo: https://github.com/pre-commit/pre-commit-hooks
        rev: v2.3.0
        hooks:
        -   id: check-yaml
        -   id: end-of-file-fixer
        -   id: trailing-whitespace
    -   repo: local
        hooks:
        -   id: black
            name: black
            entry: poetry run black
            language: system
            types: [python]
        -   id: flake8
            name: flake8
            entry: poetry run flake8
            language: system
            types: [python]
    ```
* definition of `noxfile.py` which supports: running tests, mypy (type checking), safety, flake8, black and others,
* definition of `docs` that supports `Sphinx`.

## Models

In development.
