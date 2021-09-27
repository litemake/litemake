from abc import ABC, abstractclassmethod
from litemake.printer import Color


class NodeCompilationStatus(ABC):

    @property
    @abstractclassmethod
    def color(self,) -> str:
        """ An ANSI escape code that colors text with the coressponding
        color to the compilation status (for example, the color of the
        nodes that failed to compile is red). """

    @property
    @abstractclassmethod
    def priority(self,) -> int:
        """ A positive integer that represents the priority of the compilation
        status. Larger numbers are preferred. For example, the priority of
        failed nodes should be higher than the priority of passed nodes. because
        a group with both failed and passed nodes should be presented as
        'failed'. """


class NodePassed(NodeCompilationStatus):
    color: str = Color.GREEN
    priority: int = 0


class NodeSkipped(NodeCompilationStatus):
    color: str = Color.YELLOW
    priority: int = 128


class NodeFailed(NodeCompilationStatus):
    color: str = Color.RED
    priority: int = 256
