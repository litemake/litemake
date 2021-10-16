import typing

if typing.TYPE_CHECKING:
    from .graph import CompilationFileNode  # pragma: no cover
    from .status import NodeCompilationStatus  # pragma: no cover

import litemake.exceptions
from .status import (
    NodeFailed,
    NodePassed,
    NodeSkipped,
)


class NodesCollector:
    def __init__(self, tree: "CompilationFileNode") -> None:
        self._tree = list(tree.all_nodes())
        self._status = dict()
        self._queue = (m for m in [n for n in self._tree if n.outdated_subtree])

    @property
    def count_total(
        self,
    ) -> int:
        """The number of nodes in the whole tree."""
        return len(self._tree)

    @property
    def count_outdated(
        self,
    ) -> int:
        """The nubmer of outdated nodes that need to be regenerated in the
        tree."""
        return sum(True for n in self._tree if n.outdated_subtree)

    def pop_next(
        self,
    ) -> "CompilationFileNode":
        """Pops the next node that should be compiled outside of the queue,
        and returns it. If the queue is empty, returns `None`."""

        try:
            return next(self._queue)
        except StopIteration:
            return None

    def generate(self, node: "CompilationFileNode") -> "NodeCompilationStatus":
        if self._status.get(node) is None:
            try:
                node.generate()

            except litemake.exceptions.litemakeCompilationError:
                self._status[node] = NodeFailed
                temp = node
                while temp.parent is not None:
                    self._status[temp.parent] = NodeSkipped
                    temp = temp.parent

            else:
                self._status[node] = NodePassed
        return self._status[node]
