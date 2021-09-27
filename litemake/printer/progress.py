from abc import ABC, abstractmethod

import typing
if typing.TYPE_CHECKING:
    from litemake.compile.graph import CompilationFileNode
    from litemake.compile.status import NodeCompilationStatus


class ProgressPrinter(ABC):

    @abstractmethod
    def register_status(self,
                        node: 'CompilationFileNode',
                        status: 'NodeCompilationStatus',
                        ) -> None:
        """ A method that by the main script after a node has been parsed and
        worked on. """

    @abstractmethod
    def __str__(self) -> str:
        """ Generates a string that is supposed to be printed to the console
        while litemake is compiling a target. This string should provide useful
        information to the user about the recent nodes that have been compiled.
        You can assume that this method is called and the returned string is
        printed to the console after each new node that is compiled. """
