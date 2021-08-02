# PyFixFmt

Your all-in-one python formatter. Able to be called on files or strings to format and standarize a Python file.

Removes unused imports (with [autoflake](https://github.com/myint/autoflake)), sorts imports (with [isort](https://github.com/PyCQA/isort)), and then formats the code (with [black](https://black.readthedocs.io/en/stable/)). It will respect your project's `pyproject.toml` configuration for those tools.

Meant to make formatting of python code as deterministic as sanely possible.


### Instructions

To install:

`pip install pyfixfmt`

To run:

```
# file-glob can be either a single file name or a normal unix glob.
python -m pyfixfmt --file-glob <your file glob here> --verbose
```

Configuration:

```
# in pyproject.toml
[tool.formatters.python]
# Do not change anything about imports in these files
ignore_import_changes = []
# Do not remove imports that are unused in these files
do_not_remove_imports = []
```


### Developing

Develop with [Poetry](https://python-poetry.org/).

Build with `poetry build`, and publish with `poetry publish`.