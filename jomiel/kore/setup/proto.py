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


def generate_protobuf_bindings():
    """Generates the bindings for the protobuf message declarations."""
    from ..app import exit_error

    protoc = detect_protoc()
    if not protoc:
        print('error: protoc command not found')
        exit_error()

    from subprocess import call
    from os import EX_OK

    from .cache import PROTO_FILES, PROTO_PATH  # pylint: disable=E0611
    from .echo import put

    put('Compiling the protobuf declarations for jomiel messages\n')

    for fname in PROTO_FILES:
        put('  Compiling %s...' % fname)
        args = [
            protoc, '-I' + PROTO_PATH, '--python_out=' + PROTO_PATH,
            fname
        ]
        if call(args) != EX_OK:
            exit_error()
        put(' done.\n')


def detect_protoc():
    """Try to find the protoc(1) command."""
    from os.path import exists
    from os import environ

    if 'PROTOC' in environ and exists(environ['PROTOC']):
        return environ['PROTOC']

    from distutils.spawn import find_executable  # pylint: disable=E0401,E0611
    return find_executable('protoc')


# vim: set ts=4 sw=4 tw=72 expandtab:
