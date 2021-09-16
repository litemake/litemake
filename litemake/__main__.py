import traceback
import argparse
import sys
from os import path


from . import __description__, __version__, __litemake_spec__
from .constants import DEFAULT_SETUP_FILENAME
from .printer import litemakePrinter as Printer
from .parse import SetupConfigParser as Parser
from .compile import TargetCompiler, Compiler, TargetsCollection
from .exceptions import (
    litemakeError,
    litemakeUnknownTargetsError,
)


parser = argparse.ArgumentParser(  # pylint: disable=unexpected-keyword-arg
    prog='litemake', description=__description__,
    exit_on_error=False,
    usage='litemake [options] target(s)...'
)

# TODO: implement custom argparser
parser.add_argument(
    '--version', action='store_true',
    help="show litemake's version number and exit")
parser.add_argument(
    'targets', action='store', metavar='target(s)', nargs='*',
    help='target names to run, as configured in the setup file')
parser.add_argument(
    '-f', '--file', action='store',
    help='litemake setup file',
    type=str,
    default=DEFAULT_SETUP_FILENAME,
)
parser.add_argument(
    '-d', '--directory', action='store',
    help='The directory in which litemake will run. By default, it is the ' +
    'current working directory.',
    type=str,
    default='.',
)
parser.add_argument(
    '--no-verbose', action='store_true', default=False,
    help="disables printing of commands executed by 'litemake'. " +
    "Error messages and 'litemake' summary message will still be printed.",
)


def version():
    Printer.info('\n'.join((
        f'version *{__version__}* (spec v{__litemake_spec__})',
    )))


def make(args):
    parser = Parser(path.join(args.directory, args.file))
    compiler = parser.config['litemake']['compiler']()

    litemake = parser.config['litemake']
    version = litemake['meta']['version']
    target_collection = TargetsCollection(
        package=litemake['meta']['name'],
        version=(version['major'], version['minor'], version['patch']),
        basepath=args.directory,
        outpath=litemake['output'],
        compiler=compiler,
    )

    targets = set(args.targets)
    if len(targets) == 0:
        first = next(iter(parser.config['target']))
        Printer.warning(
            f'*no explicit target:* executing first target {first!r}')

        target_config = parser.config['target'][first]
        target_collection.collect(
            # we use empty string as the target name to represent that it is
            # the default target
            target=str(),
            library=target_config['library'],
            sources=target_config['sources'],
            includes=target_config['include'],
        )

    else:
        known_targets = set(parser.config['target'].keys())
        unknown_targets = targets - known_targets

        if unknown_targets:
            raise litemakeUnknownTargetsError(unknown_targets)

        for name in targets:
            target_config = parser.config['target'][name]
            target_collection.collect(
                target=name,
                library=target_config['library'],
                sources=target_config['sources'],
                includes=target_config['include'],
            )

    target_collection.make()


def main():
    args = parser.parse_args()
    Printer.set_verbose(not args.no_verbose)

    if args.version:
        version()
        sys.exit(0)

    try:
        make(args)
        sys.exit(0)

    except litemakeError as error:
        error.print()
        sys.exit(1)

    except Exception:  # pylint: disable=broad-except

        # Remove first line from message:
        # "Traceback (most recent call last)"
        err_lines = traceback.format_exc(limit=3).splitlines()
        err = '\n'.join(err_lines[1:])

        # Print coresponding message and exit with error code 2
        msg = f'*unexpected error:*\n{err}'
        Printer.error(msg)
        sys.exit(2)


if __name__ == '__main__':
    main()
