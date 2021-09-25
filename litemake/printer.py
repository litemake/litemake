''' printer.py - litemake - Alon Krymgand Osovsky (2021)

    A class that takes care of all printing done by litemake. '''

import re
import typing


class Color:
    """ A simple class that wraps the ANSI color escape codes used by
    litemake. """

    BLACK = '\u001b[30m'
    RED = '\u001b[31m'
    GREEN = '\u001b[32m'
    YELLOW = '\u001b[33m'
    BLUE = '\u001b[34m'
    MAGENTA = '\u001b[35m'
    CYAN = '\u001b[36m'
    WHITE = '\u001b[37m'
    GREY = '\u001b[90m'

    BOLD = '\u001b[1m'
    UNDERLINE = '\u001b[4m'
    REVERSED = '\u001b[7m'

    RESET = '\u001b[0m'


class litemakePrinter:

    TITLE = Color.BOLD + Color.BLUE + 'litemake:' + Color.RESET
    PADDING = ' ' * 2

    @staticmethod
    def replace_special(original: str, repl: str):
        return re.sub(r'\*(.*?)\*', repl.replace('%s', r'\g<1>'), original)

    @classmethod
    def print(cls, text: str) -> None:
        lines = text.splitlines()

        # print first line
        print(cls.TITLE + ' ' + lines.pop(0).strip())

        # print other lines
        for line in lines:
            print(cls.PADDING + line)

    @classmethod
    def debug(cls, info: str) -> None:
        msg = cls.replace_special(
            info, f'{Color.BOLD}%s{Color.RESET}{Color.GREY}')
        cls.print(f'{Color.GREY}{msg}{Color.RESET}')

    @classmethod
    def info(cls, info: str) -> None:
        info = cls.replace_special(info, f'{Color.BOLD}%s{Color.RESET}')
        cls.print(info)

    @classmethod
    def summary(cls, summary: str) -> None:
        special = f'{Color.BOLD}{Color.GREEN}%s{Color.RESET}'
        summary = cls.replace_special(summary, special)
        cls.print(summary)

    @classmethod
    def warning(cls, warning: str) -> None:
        special = f'{Color.BOLD}{Color.YELLOW}%s{Color.RESET}'
        warning = cls.replace_special(warning, special)
        cls.print(warning)

    @classmethod
    def error(cls, error: str) -> None:
        special = f'{Color.RED}{Color.BOLD}%s{Color.RESET}'
        error = cls.replace_special(error, special)
        cls.print(error)

    @classmethod
    def command(cls, cmd: typing.List[str]) -> None:
        """ Called by the 'compiler' object when a compelation process begins. """
        cls.debug('\n'.join((
            '*executing command:*',
            ' '.join(cmd),
        )))
