# -*- coding: utf-8 -*-

from distutils.core import setup


with open('LICENSE') as f:
    license = f.read()

setup(
    name='hydro_borg',
    version='0.0.1',
    author='Stefan Lüdtke',
    url='https://git.gfz-potsdam.de:sluedtke/borg_hydro.git',
    packages=['swimpy'],
    py_modules=['config', 'utils', 'gof_python'],
    license=license
)
