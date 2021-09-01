import traceback
import argparse
import sys


from . import __description__, __version__, __nanomake_spec__
from .printer import NanomakePrinter as Printer
from .exceptions import NanomakeError
from .parse import SetupConfigParser as Parser

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


def make(args):
    parser = Parser(args.file)
    print(parser.raw)


def main():
    args = parser.parse_args()

    if args.version:
        version()
        sys.exit(0)

    try:
        make(args)
        sys.exit(0)

    except NanomakeError as error:
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
