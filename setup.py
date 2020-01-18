#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# jomiel
#
# Copyright
#  2019-2020 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#
"""setup.py for jomiel."""

# Supported env. definitions:
#   - VERSION_TIME to append "%H%M" to the version number
#
PACKAGE_NAME = "jomiel"
GITHUB_ADDR = "https://github.com/guendto/%s/" % PACKAGE_NAME

from sys import path

path.insert(0, ".")

# Initialize by calling kore.setup:init(). Do this before importing the
# custom commands below.
#
from jomiel.kore.setup import init as setup_init

setup_init(
    name=PACKAGE_NAME,
    bootstrap_path="%s/comm/proto/bin/bootstrap" % PACKAGE_NAME,
    proto_root_dir="%s/comm/proto/" % PACKAGE_NAME,
    bindings_dir="bindings",  # jomiel/data/bindings (*_pb2.py files)
    data_dir="data",  # jomiel/data (VERSION file, etc.)
)

from jomiel.kore.setup.cmd import CustomCommand__bdist_wheel
from jomiel.kore.setup.cmd import CustomCommand__build_py
from jomiel.kore.setup.cmd import CustomCommand__clean

# from jomiel.kore.setup.cmd import CustomCommand__sdist

from jomiel.kore.setup.version import get_semantic_version
from jomiel.kore.setup.file import read_file

requirements = read_file("requirements.in").splitlines()

# setup()
#
from setuptools import setup, find_namespace_packages

setup(
    name=PACKAGE_NAME,
    author="Toni Gündoğdu",
    author_email="<>",
    version=get_semantic_version(),
    description="Meta inquiry middleware for distributed systems",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url=GITHUB_ADDR,
    packages=find_namespace_packages(include=["jomiel.*"], exclude=[])
    + ["jomiel"],
    # Note how we append "jomiel" to the "packages" list after looking
    # up the namespace packages. We do this because of the way we have
    # structured the project. find_namepace_packages() fails to add any
    # of the ./jomiel/*.py files.
    #
    include_package_data=True,
    # There are plenty of confusing and conflicting resources around,
    # many of which offer different ideas on how you should use:
    #   - include_package_data
    #   - MANIFEST.in
    #   - setup.py
    #
    # Throw the protobuf compilation into the mix and you'll begin to
    # wonder why even bother with packaging at all.
    #
    # After spending far more time than anyone ever should -- for
    # something as simple as this -- it seems that we have found
    # ourselves a winner combo through great many trials and errors.
    # And that, is good enough for me.
    #   -- the author
    #
    python_requires=">=3.6",
    install_requires=read_file("requirements.in").splitlines(),
    entry_points={
        "console_scripts": [
            "jomiel=jomiel:main",
            "jomiel-keygen=jomiel.keygen:main",
        ]
    },
    cmdclass={
        "bdist_wheel": CustomCommand__bdist_wheel,
        "build_py": CustomCommand__build_py,
        #        "sdist": CustomCommand__sdist,
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
