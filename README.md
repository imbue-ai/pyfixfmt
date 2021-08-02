# PyFixFmt

A simple python formatter.

Just removes unused imports (with [autoflake](https://github.com/myint/autoflake)), sorts imports (with [isort](https://github.com/PyCQA/isort)), and then formats the code (with [black](https://black.readthedocs.io/en/stable/)).

Meant to make formatting of python code as deterministic as sanely possible.


### Instructions

To run:

```
$ # Recommended way, since it should work from wherever it's installed
$ python -m pyfixfmt --file-glob <your file glob here> --verbose

$ # Or, since I'm a nice guy
$ python pyfixfmt --file-glob <your file glob here> --verbose

```
