# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup
import qsmell

if sys.hexversion < 0x3000000:
    print('QSmell requires Python 3.0 or newer!')
    sys.exit()

dir = os.path.dirname(os.path.abspath(__file__))
version = {}
with open(os.path.join(dir, "qsmell", "version.py")) as fp:
    exec(fp.read(), version)

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md') as f:
    long_description = f.read()

setup(
    name='QSmell',
    version=version["__version__"],
    python_requires='>=3.0',
    description='QSmell is a tool for detecting quantum-based code smells in programs written in the Qiskit framework.',
    long_description=long_description,
    author='<retracted>',
    author_email='<retracted>',
    url='<retracted>',
    download_url='<retracted>',
    packages=['qsmell', 'qsmell.smell'],
    package_data={'qsmell': ['data/*']},
    entry_points={
        "console_scripts": ['qsmell = qsmell.cli:main']
    },
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
    ],
)