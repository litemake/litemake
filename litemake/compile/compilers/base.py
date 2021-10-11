import typing
import subprocess
from abc import ABC, abstractmethod

from litemake.exceptions import litemakeCompilationError


class AbstractCompiler(ABC):
    def _exec_cmd(self, *cmd) -> None:
        """Recives a command that is represented as a list of arguments,
        and runs it in a new subprocess. Raises an error if the return code
        from the subprocess is a non-zero one."""

        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
        )

        if result.returncode != 0:
            raise litemakeCompilationError(
                subprocess=cmd[0],
                msg=result.stderr,
            )

    @property
    @staticmethod
    @abstractmethod
    def name(self) -> str:
        """Return a string that represents the compiler class. Typically,
        the name will also be the first command line argument when calling
        the compiler."""

    @property
    @staticmethod
    @abstractmethod
    def required_clis() -> typing.Set[str]:
        """Returns a list of strings that represent names of required CLIs
        to run this compiler successfully."""

    @abstractmethod
    def create_obj(self, src: str, dest: str, includes: typing.List[str]) -> None:
        """Compile the given source C/C++ file into a object file."""

    @abstractmethod
    def create_archive(self, dest: str, objs: typing.List[str]) -> None:
        """Combine the given object files into a single archive (static
        library) file."""

    @abstractmethod
    def create_executable(self, dest: str, archives: typing.List[str]) -> None:
        """Combine multiple archives into a single executable."""
