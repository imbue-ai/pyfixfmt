# PyFixFmt

A simple python formatter.

Just removes unused imports (with [autoflake](https://github.com/myint/autoflake)), sorts imports (with [isort](https://github.com/PyCQA/isort)), and then formats the code (with [black](https://black.readthedocs.io/en/stable/)).

Meant to make formatting of python code as deterministic as sanely possible.


### Instructions

To install:

`pip install pyfixfmt`

To run:


Recommended way, since it should work from wherever

`python -m pyfixfmt --file-glob <your file glob here> --verbose`

Or, to run without installing

`python pyfixfmt --file-glob <your file glob here> --verbose`


file-glob can be either a single file name or a normal unix glob.
