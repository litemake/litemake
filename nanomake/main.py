import argparse
import sys

from . import __description__, __version__, __nanomake_spec__
from .printer import NanomakePrinter as Printer

parser = argparse.ArgumentParser(
    prog='nanomake', description=__description__,
    exit_on_error=False,
    usage='nanomake [options] target(s)...'
)

parser.add_argument(
    '--version', action='store_true',
    help="show nanomake's version number and exit")
parser.add_argument(
    'targets', action='store', metavar='target(s)', nargs='*',
    help='target names to run, as configured in the setup file')
parser.add_argument(
    '-f', '--file', action='store',
    help='nanomake setup file',
    type=str,
    default='setup.nanomake.toml',
)
parser.add_argument(
    '-v', '--verbose', action='store_true', default=False,
    help='prints the commands that nanomake executes',
)


def version():
    Printer.info('\n'.join((
        f'version *{__version__}* (spec v{__nanomake_spec__})',
    )))


def main(args):

    if args.version:
        version()
        sys.exit(0)


if __name__ == '__main__':
    main(parser.parse_args())
