#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# jomiel
#
# Copyright
#  2019 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#
"""setup.py for jomiel."""

from sys import path

path.insert(0, ".")

# Enable VERSION_TIME to append "%H%M" to the version number.
#

from setuptools import setup, find_packages
from jomiel.kore.setup import init as setup_init

setup_init(  # Do this before the import lines for "cmd" below.
    "jomiel", "comm/proto"
)

from jomiel.kore.setup.cmd import CustomCommand__bdist_wheel
from jomiel.kore.setup.cmd import CustomCommand__build_py
from jomiel.kore.setup.cmd import CustomCommand__sdist
from jomiel.kore.setup.cmd import CustomCommand__clean

from jomiel.kore.setup.version import get_semantic_version
from jomiel.kore.setup.file import read_file

GITHUB_ADDR = "https://github.com/guendto/jomiel/"

setup(
    name="jomiel",
    author="Toni Gündoğdu",
    author_email="<>",
    version=get_semantic_version(),
    description="Meta inquiry middleware for distributed systems",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url=GITHUB_ADDR,
    packages=find_packages(exclude=[]),
    package_data={
        "jomiel": [
            "config/logger/jomiel.yaml",
            "VERSION",
            # Issue:
            #   - The 'build' stage fails to find the generated *_pb2.py
            #   files, even when 'build_py' target is built first
            # Workaround:
            #   - Force the inclusion of 'comm/proto/*.py files here so that
            #   they are included
            #
            "comm/proto/*.py",
        ],
    },
    python_requires=">=3.5",
    install_requires=[
        "configargparse",
        "protobuf",
        "pyzmq",
        "requests",
        "ruamel.yaml",
        "validators",
    ],
    entry_points={
        "console_scripts": [
            "jomiel=jomiel:main",
            "jomiel-keygen=jomiel.keygen:main",
        ]
    },
    cmdclass={
        "bdist_wheel": CustomCommand__bdist_wheel,
        "build_py": CustomCommand__build_py,
        "sdist": CustomCommand__sdist,
        "clean": CustomCommand__clean,
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ],
    project_urls={
        "Bug Reports": "%s/issues" % GITHUB_ADDR,
        "Source": GITHUB_ADDR,
    },
)

# vim: set ts=4 sw=4 tw=72 expandtab:
