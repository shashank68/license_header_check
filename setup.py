from setuptools import find_packages
from setuptools import setup

setup(
    name='License Header check pre-commit hook',
    description='Fixes license header of python files',
    version='1.1',
    packages=find_packages('.'),
    entry_points={
        'console_scripts': [
            'license_check=license_header_check.license_check:main',
        ],
    },
)