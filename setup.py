# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


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
    tests_require=['pytest'],
    install_requires=['pandas', 'numpy', 'jsonschema']
)
