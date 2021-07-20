# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfixfmt']

package_data = \
{'': ['*']}

install_requires = \
['autoflake>=1.3.1,<2.0.0', 'black>=19.10b0,<20.0', 'isort>=4.3.21,<5.0.0']

setup_kwargs = {
    'name': 'pyfixfmt',
    'version': '0.9.0',
    'description': 'Run several python fixers over a python file.\n\nIt will respect the settings in your `pyproject.toml`.\n\nProvides both a file-based and string-based API, as well as able\nto be run from the command line.\n',
    'long_description': "# PyFixFmt\n\nPython Format Fixer.\n\n\n### Instructions\n\nTo run:\n\n```\n$ # Recommended way, since it should work from wherever it's installed\n$ python -m pyfixfmt --file-glob <your file glob here> --verbose\n\n$ # Or, since I'm a nice guy\n$ python pyfixfmt --file-glob <your file glob here> --verbose\n\n```\n",
    'author': 'TJ DeVries',
    'author_email': 'devries.timothyj@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'TODO',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
