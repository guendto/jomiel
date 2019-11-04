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

from abc import ABCMeta, abstractmethod
from importlib import import_module
from sys import stdout


class App:
    """A simple core class that wraps all-things-necessary to create
    command line interface application with very little effort."""

    __slots__ = [
        '_no_default_config_files',
        '_no_config_file_option',
        '_pkg_resources_name',
        '_no_logger_options',
        '_no_print_config',
        '_config_module',
        '_logger_files',
        '_version',
    ]

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        """Initializes the object.

        Args:
            **kwargs: arbitrary keyword args

        Supported arbitrary keyword args (kwargs):

            module_name (str): The name of the module, e.g. __name__
                This value will be used to determine the different XDG
                configuration file paths.

            version (str): The program version string, if undefined, the
                the version string is formatted from the output `git
                show`.

            no_print_config (bool): If True, disables the -D nor -E
                options

            no_default_config_files (bool): If True, disables the
                use of the default (XDG) configuration files

            no_config_file_option (bool): If True, disables the support
                for the --config-file option

            no_logger_options (bool): If True, disables the support
                for logger features (e.g. --logger-file, --logger-ident)

            config_module (str): Path to the configuration module that will
                be imported and accessed throughout the app life-cycle.

            pkg_resources_name (str): Used with pkg_resources to query
                access to the data installed with the app, if left
                undefined, pkg_resource queries are completely skipped.

                Needed to retrieve information about the installed
                version of the application.

                The value is usually set to __name__.

        """
        self._no_logger_options = kwargs.get('no_logger_options', False)
        self._no_print_config = kwargs.get('no_print_config', False)
        self._pkg_resources_name = kwargs.get('pkg_resources_name')
        self._config_module = kwargs.get('config_module')

        self._no_default_config_files = kwargs.get(
            'no_default_config_files', False)

        self._no_config_file_option = kwargs.get(
            'no_config_file_option', False)

        def determine_xdg_paths():
            """Return the XDG paths to configuration files."""
            module_name = kwargs.get('module_name')

            if not module_name or self._no_default_config_files:
                return ([], [])

            config_files = [
                '/etc/xdg/{0}/{0}.yaml'.format(module_name),
                '~/.config/{0}/{0}.yaml'.format(module_name),
                './{}.yaml'.format(module_name)
            ]

            logger_files = [
                '/etc/xdg/{}/logger.yaml'.format(module_name),
                '~/.config/{}/logger.yaml'.format(module_name),
                './logger.yaml'
            ]

            if self._pkg_resources_name:
                from pkg_resources import resource_filename

                config_path = 'config/logger/%s.yaml' % module_name

                resource_fname = resource_filename(
                    self._pkg_resources_name, config_path)

                logger_files.insert(0, resource_fname)

            return (config_files, logger_files)

        def determine_version():
            """Return the app version string.

            Unless kwargs 'version' was given, tries to determine the
            version from different sources. See `try_version` function
            for more details.

            """
            version = kwargs.get('version')

            if not version:
                from .version import try_version
                version = try_version(self._pkg_resources_name)

            if isinstance(version,
                          list):  # Value read from VERSION file
                return version

            return (version, None)

        (config_files, self._logger_files) = determine_xdg_paths()
        self._version = determine_version()

        from configargparse import get_parser
        parser = get_parser(default_config_files=config_files,
                            add_config_file_help=False)

        parser.add('--version',
                   action='version',
                   version='%(prog)s version ' + self._version[0])

        parser.add('-v',
                   '--version-long',
                   help="""show version information about program's
                    environment and exit""",
                   action='store_true')

        if not self._no_config_file_option:
            parser.add(
                '--config-file',
                help='Read configuration from the specified file',
                is_config_file=True,
                metavar='FILE')

        if not self._no_print_config:
            parser.add('-D',
                       '--print-config',
                       help='Show the configuration values and exit',
                       action='store_true')

            parser.add(
                '-E',
                '--report-config',
                help='Report keys, values and where they were set',
                action='store_true')

        def logger_group():
            """Add the logger option group."""
            grp = parser.add_argument_group('logger')

            grp.add('--logger-config',
                    help='Logger configuration file to read',
                    metavar='FILE')

            grp.add('-L',
                    '--logger-idents',
                    help='Print logger identities and exit',
                    action='store_true')

            grp.add(
                '--logger-idents-verbose',
                help=
                'Print logger identities in detail, use together with --logger-idents',
                action='store_true')

            grp.add('-l',
                    '--logger-ident',
                    help='Use the logger identity',
                    metavar='IDENT',
                    default='default')

        if not self._no_logger_options:
            logger_group()

    @abstractmethod
    def run(self):
        """[Override] Runs the program."""
    def parse_opts(self, parser):
        """Parses the options.

        Notes:
            - Handles the -D and -E options gracefully

            - Applications subclassing this class, do not need to
              implement the support

            - Instead, the these are either disabled by the subclass or
              handled automagically by the superclass

        Args:
            parser (obj): configargparse parser instance

        """
        def handle_print_config():
            """Handle the -D and -E options."""

            if self._no_print_config:
                return

            def print_config_values(opts):
                """Prints the configuration values to stdout and
                terminate the program.

                Args:
                    opts (dict): configargparse returned options

                """
                data = {
                    'configuration': opts.__dict__,
                }
                dump_as_yaml(data)

            def print_report_config(parser):
                """Prints the configuration sources to stdout and
                terminates the program.

                Args:
                    parser (obj): configargparse parser instance

                """
                parser.print_values()
                exit_normal()

            if opts.print_config:
                print_config_values(opts)

            elif opts.report_config:
                print_report_config(parser)

        def handle_version_long():
            """Handle --version-long"""

            if not opts.version_long:
                return

            def version_long():
                """Return string to be printed with --version-long"""
                def module_versions():
                    """Return the module versions."""
                    from .version import format_module_version

                    required_modules = self.version_long_modules()
                    found_modules = []

                    for module_name in sorted(required_modules.keys()):
                        format_module_version(
                            module_name, required_modules[module_name],
                            found_modules)

                    return [{
                        key: value
                    } for key, value in found_modules]

                def app_version():
                    """Return the application version."""
                    if self._version[1]:  # Has 'packaged' version.
                        version = {
                            'semantic': self._version[0].strip(),
                            'packaged': self._version[1].strip()
                        }
                    else:
                        version = self._version[0]
                    return version

                from sys import version as py_version

                return {
                    'version': app_version(),
                    'python': {
                        'version': py_version.replace('\n', ''),
                        'modules': module_versions(),
                    }
                }

            yaml = version_long()
            dump_as_yaml(yaml)

        def setup_global_config():
            """Sets up the global config module with the parsed options."""

            if not self._config_module:
                return

            mod = import_module(self._config_module)

            if opts.logger_config:
                self._logger_files.insert(0, opts.logger_config)

            mod.logger_paths = self._logger_files
            mod.opts = opts

        opts = parser.parse()

        handle_print_config()
        handle_version_long()

        setup_global_config()

        return opts

    def version_long_modules(self):  # pylint: disable=R0201
        """[Override] Returns the required modules that we wish to check
        with --version-long and append to the output.

        Note:
            - Override this in your applications

        Returns:
            dict: of module names (empty)

            Example:
                return {'requests': 'Requests',
                        'yaml': 'PyYAML',
                        'zmq': 'PyZMQ'}

        """
        return {}


def subprocess_open(args):
    """Execute subprocess by using Popen."""
    from subprocess import Popen, PIPE
    chld = Popen(args, stdout=PIPE)
    data = chld.communicate()[0]
    return (chld.returncode, data.rstrip().decode('utf8'))


def exit_with(code):
    """Calls sys.exit with the exit status code."""
    from sys import exit as _exit
    _exit(code)


def exit_error():
    """Wraps the sys.exit call, exits with an error status code (1)."""
    exit_with(1)


def exit_normal():
    """Wraps the sys.exit call, exits with an OK status code (0)."""
    exit_with(0)


def round_trip_dump_yaml(data, stream=None):
    """Dump YAML.

    Args:
        data (dict): to be dumped as YAML
        stream (obj): to dump the YAML to

    """
    from ruamel.yaml import YAML, round_trip_dump
    yaml = YAML(typ='safe')
    yaml.default_flow_style = False
    round_trip_dump(data, stream)


def dump_as_yaml(yaml):
    """Dump the given data as YAML to stdout and exit process.

    Args:
        yaml (dict): data to be dumped

    """
    stdout.write('---\n')
    round_trip_dump_yaml(yaml, stdout)
    exit_normal()


def dump_logger_identities(loggers, detailed=False):
    """Dump the found logger identities to the stdout and exit.

    Args:
        loggers (dict): from the parsed .yaml to be dumped
        detailed (bool): be detailed

    """
    idents = loggers if detailed else [ident for ident in loggers]
    yaml = {'identities': idents}
    dump_as_yaml(yaml)


# vim: set ts=4 sw=4 tw=72 expandtab:
