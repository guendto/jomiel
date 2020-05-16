#
# jomiel-kore
#
# Copyright
#  2019-2020 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#
"""TODO."""
from distutils.command.clean import clean

from setuptools.command.build_py import build_py
from wheel.bdist_wheel import bdist_wheel

# from setuptools.command.sdist import sdist
#
# class CustomCommand__sdist(sdist):
#    # Custom command for setup target sdist. Triggers build_py.
#
#    def run(self):
#        # run
#        self.run_command("build_py")
#        return sdist.run(self)


class CustomCommand__bdist_wheel(bdist_wheel):
    """Custom command for setup target bdist_wheel. Triggers build_py."""

    def run(self):
        """run"""
        self.run_command("build_py")
        return bdist_wheel.run(self)


class CustomCommand__build_py(build_py):
    """Custom command for setup target build_py."""

    def run(self):
        """run"""
        from .cache import (
            BOOTSTRAP_PATH,
            PROTO_ROOT_DIR,
            DATA_BINDINGS_DIR,
        )
        from .proto import compile_protobuf_bindings
        from .version import save_version_file
        from .file import touch_file

        compile_protobuf_bindings(
            BOOTSTRAP_PATH, PROTO_ROOT_DIR, DATA_BINDINGS_DIR,
        )

        def packagistize_bindings_dir():
            """Add the missing __init__.py file to the bindings dir."""
            from os.path import join, sep

            path = DATA_BINDINGS_DIR.replace(".", sep)
            tmp = join(path, "__init__.py")
            print("tmp", tmp)
            touch_file(join(path, "__init__.py"))

        packagistize_bindings_dir()
        save_version_file()

        return build_py.run(self)


class CustomCommand__clean(clean):
    """Custom command for setup target clean."""

    def run(self):
        """run"""
        from .cache import DATA_VERSION_FILE
        from distutils.debug import DEBUG
        from os.path import sep
        from ..file import unlink_if

        files = [DATA_VERSION_FILE.replace(".", sep)]

        for _file in files:
            unlink_if(_file, verbose=DEBUG)

        def clean_all():
            """`setup.py clean` was called with `--all`.

            Remove anything that wasn't removed. Get inspired:
              https://blog.ionelmc.ro/2014/06/25/python-packaging-pitfalls/

            """
            from distutils.dir_util import remove_tree
            from os.path import isdir, sep
            from .cache import NAME, DATA_BINDINGS_DIR

            def rmtree_if(dirname):
                """Remove tree conditionally."""
                if isdir(dirname):
                    remove_tree(dirname)

            dirs = [
                NAME + ".egg-info",
                "build",
                DATA_BINDINGS_DIR.replace(".", sep),
            ]

            for _dir in dirs:
                rmtree_if(_dir)

        rval = clean.run(self)  # Run the default handler first

        if self.all:  # `--all` was given
            clean_all()

        return rval


# vim: set ts=4 sw=4 tw=72 expandtab:
