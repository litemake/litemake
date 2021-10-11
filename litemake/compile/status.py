from abc import ABC, abstractclassmethod
from litemake.printer import Color


class NodeCompilationStatus(ABC):

    __statuses = set()

    def __init_subclass__(cls):
        NodeCompilationStatus.__statuses.add(cls)

    @staticmethod
    def registered_statuses():
        """Returns all nodes that have been registered (inherited from
        the 'NodeCompilationStatus' class) in their order of priority (
        lowest priority first)."""
        return sorted(NodeCompilationStatus.__statuses, key=lambda node: node.priority)

    @property
    @abstractclassmethod
    def title(
        self,
    ) -> str:
        """A string that represents the title (name) of the status."""

    @property
    @abstractclassmethod
    def color(
        self,
    ) -> str:
        """An ANSI escape code that colors text with the coressponding
        color to the compilation status (for example, the color of the
        nodes that failed to compile is red)."""

    @property
    @abstractclassmethod
    def priority(
        self,
    ) -> int:
        """A positive integer that represents the priority of the compilation
        status. Larger numbers are preferred. For example, the priority of
        failed nodes should be higher than the priority of passed nodes. because
        a group with both failed and passed nodes should be presented as
        'failed'."""


class NodePassed(NodeCompilationStatus):
    title: str = "passed"
    color: str = Color.GREEN
    priority: int = 0


class NodeSkipped(NodeCompilationStatus):
    title: str = "skipped"
    color: str = Color.YELLOW
    priority: int = 128


class NodeFailed(NodeCompilationStatus):
    title: str = "failed"
    color: str = Color.RED
    priority: int = 256
