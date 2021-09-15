import typing
import subprocess
from abc import ABC, abstractmethod

from litemake.exceptions import litemakeCompilationError
from litemake.printer import litemakePrinter as Printer


class AbstractCompiler(ABC):

    def _exec_cmd(self, *cmd) -> None:
        """ Recives a command that is represented as a list of arguments,
        and runs it in a new subprocess. Prints the command if the printer
        verbose option is set to `True` and raises an error if the return code
        from the subprocess is a non-zero one. """

        Printer.command(cmd)
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise litemakeCompilationError(
                subprocess=cmd[0],
                msg=result.stderr,
            )

    @abstractmethod
    def create_obj(self, src: str, dest: str):
        """ Compile the given source C/C++ file into a object file. """

    @abstractmethod
    def create_archive(self, dest: str, objs: typing.List[str]):
        """ Combine the given object files into a single archive (static
        library) file. """

    @abstractmethod
    def create_exectutable(self, dest: str, archives: typing.List[str]):
        """ Combine multiple archives into a single exectutable. """
