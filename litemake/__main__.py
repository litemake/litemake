import traceback
import argparse
import sys


from . import __description__, __version__, __litemake_spec__
from .printer import litemakePrinter as Printer
from .exceptions import litemakeError
from .parse import SetupConfigParser as Parser
from .compiler import litemakeCompiler as Compiler

parser = argparse.ArgumentParser(
    prog='litemake', description=__description__,
    exit_on_error=False,
    usage='litemake [options] target(s)...'
)

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
    default='setup.litemake.toml',
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
    parser = Parser(args.file)

    compiler = Compiler(
        src='.',
        dest=parser.config['litemake']['output'],
        compiler=parser.config['litemake']['compiler'],
        flags=parser.config['litemake']['flags'],
        objext=parser.config['litemake']['objext'],
        srcext=parser.config['litemake']['srcext'],
    )


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
