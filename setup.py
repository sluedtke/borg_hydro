# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import sys

# Because it uses Setuptools setup_requires, pytest-runner will install itself
# on every invocation of setup.py. In some cases, this causes delays for
# invocations of setup.py that will never invoke pytest-runner. To help avoid
# this contingency, consider requiring pytest-runner only when pytest is
# invoked:
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

with open('LICENSE') as f:
    license = f.read()

setup(
    name='borg_hydro',
    version='0.0.1',
    author='Stefan Lüdtke',
    url='https://git.gfz-potsdam.de:sluedtke/borg_hydro.git',
    packages=find_packages(),
    license=license,
    include_package_data=True,
    setup_requires=[
        'pytest-runner'
        ],
    tests_require=[
        'pytest'
        ],
    install_requires=[
        'pandas', 'numpy', 'jsonschema'
        ]
)
