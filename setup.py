#!/usr/bin/env python

"""The setup script."""

from setuptools import setup

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

with open('README.md', 'r') as fh:
    long_description = fh.read()

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Topic :: Scientific/Engineering',
]

setup(
    name='esmcol-validator',
    long_description_content_type='text/markdown',
    description='A package to validate ESM Collection files',
    long_description=long_description,
    python_requires='>=3.6',
    maintainer='Anderson Banihirwe',
    maintainer_email='abanihi@ucar.edu',
    classifiers=CLASSIFIERS,
    url='https://github.com/NCAR/esm-collection-spec',
    packages=['esmcol_validator'],
    include_package_data=True,
    install_requires=install_requires,
    license='Apache 2.0',
    zip_safe=False,
    entry_points={'console_scripts': ['esmcol-validator = esmcol_validator.cli:main']},
    keywords='intake, esm, catalog',
    use_scm_version={'version_scheme': 'post-release', 'local_scheme': 'dirty-tag'},
    setup_requires=['setuptools_scm', 'setuptools>=30.3.0'],
)
