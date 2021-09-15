import pytest
from litemake.printer import litemakePrinter as Printer

Printer.set_verbose(True)  # initialize to default value


class change_verbose:
    """ An object that is responsible for managing and changing the Printer's
    verbose mode, when it is required by the tests. """

    def __init__(self, mode: bool, printer):
        self.printer = printer
        self.new = mode
        self.old = None

    def __enter__(self):
        self.old = self.printer.verbose
        self.printer.set_verbose(self.new)

    def __exit__(self, *_):
        if self.old is not None:
            self.printer.set_verbose(self.old)
            self.old = None


@pytest.mark.parametrize('text', ('Hello there!',))
class TestPrinter:

    def test_printer_no_debug_when_verbose_off(self, text, capsys):
        with change_verbose(False, Printer):
            Printer.debug(text)

        assert len(capsys.readouterr().out) == 0
