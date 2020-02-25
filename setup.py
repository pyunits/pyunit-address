#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2020/2/18 15:23
# @Author: Jtyoui@qq.com
from setuptools import setup, find_packages
from pyunit_address import __version__, __author__, __description__, __email__, __names__, __url__

with open('README.md', encoding='utf-8') as f:
    long_text = f.read()

with open('requirements.txt', encoding='utf-8') as f:
    install_requires = f.read().strip().splitlines()

setup(
    name=__names__.lower(),
    version=__version__,
    description=__description__,
    long_description=long_text,
    long_description_content_type="text/markdown",
    url=__url__,
    author=__author__,
    author_email=__email__,
    license='MIT Licence',
    packages=find_packages(),
    platforms='any',
    package_data={'': ['*']},
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=True,
)
