''' printer.py - nanomake - Alon Krymgand Osovsky (2021)

    A class that takes care of all printing done by nanomake. '''

import re


class Color:
    """ A simple class that wraps the ANSI color escape codes used by
    nanomake. """

    BLACK = u'\u001b[30m'
    RED = u'\u001b[31m'
    GREEN = u'\u001b[32m'
    YELLOW = u'\u001b[33m'
    BLUE = u'\u001b[34m'
    MAGENTA = u'\u001b[35m'
    CYAN = u'\u001b[36m'
    WHITE = u'\u001b[37m'

    BOLD = u'\u001b[1m'
    UNDERLINE = u'\u001b[4m'
    REVERSED = u'\u001b[7m'

    RESET = u'\u001b[0m'


class NanomakePrinter:

    TITLE = Color.BOLD + Color.BLUE + 'nanomake:' + Color.RESET
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
            print(cls.PADDING + line.strip())

    @classmethod
    def info(cls, info: str) -> None:
        info = cls.replace_special(info, f'{Color.BOLD}%s{Color.RESET}')
        cls.print(info)

    @classmethod
    def warning(cls, warning: str) -> None:
        special = f'{Color.BOLD}{Color.MAGENTA}%s{Color.RESET}'
        warning = cls.replace_special(warning, special)
        cls.print(warning)

    @classmethod
    def error(cls, error: str) -> None:
        special = f'{Color.RED}{Color.BOLD}{Color.UNDERLINE}%s{Color.RESET}'
        error = cls.replace_special(error, special)
        cls.print(error)
