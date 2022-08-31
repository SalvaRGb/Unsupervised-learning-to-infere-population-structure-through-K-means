from setuptools import setup
from setuptools import find_packages

setup(
    name = 'HapMap_organizer',
    version = '1.0.0',
    description = 'This package contains a hapmap class fto help filtering short hapmap files',
    author = 'SalvaRGb',
    packages = find_packages(),
    install_requires = ['numpy', 'pandas', 'scikit-learn']
    )
    