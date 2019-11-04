# -*- coding: utf-8 -*-
#
# jomiel-kore
#
# Copyright
#  2019 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#
"""TODO."""


def set_proto_path(loaded_from_module_path, proto_path):
    """Include proto dir in sys.path search path.

    The function constructs a full path to the give proto dir residing
    in the source tree. The only reason this function exists:
        - https://github.com/protocolbuffers/protobuf/issues/762
        - https://github.com/protocolbuffers/protobuf/issues/881
        - https://github.com/protocolbuffers/protobuf/issues/957
        - https://github.com/protocolbuffers/protobuf/issues/1491

    Args:
        loaded_from_module_path (str): the pathname of the file from
            which the module was loaded, e.g. __file__

        proto_path (str): the path to the proto dir where the .proto
            files reside

    """
    from os.path import dirname, abspath, join

    pkg_dir = dirname(abspath(loaded_from_module_path))
    proto_dir = join(pkg_dir, proto_path)

    from sys import path

    path.insert(2, proto_dir)


# vim: set ts=4 sw=4 tw=72 expandtab:
