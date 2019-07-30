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
"""TODO."""


def init():
    """Initiates the logging subsystem."""
    from jomiel.cache import logger_paths, opts  # pylint: disable=E0611
    from jomiel import lg

    def disable_logging_if():
        return opts.plugin_list or opts.logger_idents

    lg().disabled = disable_logging_if()

    from jomiel.kore.log import log_init
    (logger_file, logger_idents) = log_init(logger_paths)

    lg().debug('subsys/log: configuration file loaded from \'%s\'',
               logger_file)

    lg().info('log subsystem initiated')

    if opts.logger_idents:
        print(''.join('%s' % [ident for ident in logger_idents]))
        from jomiel.kore.app import exit_normal
        exit_normal()


# vim: set ts=4 sw=4 tw=72 expandtab:
