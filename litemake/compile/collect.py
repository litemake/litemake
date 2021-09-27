import typing
if typing.TYPE_CHECKING:
    from .graph import CompilationFileNode
    from .status import NodeCompilationStatus

from .status import (
    NodeFailed,
    NodePassed,
    NodeSkipped,
)
from litemake.exceptions import litemakeCompilationError

from functools import cached_property


class NodesCollector:

    def __init__(self, tree: 'CompilationFileNode') -> None:
        self._queue = (n for n in tree.all_nodes() if n.outdated_subtree)
        self._status = dict()

    @property
    def count(self,) -> int:
        """ The number of nodes in the whole tree. """
        return len(self.nodes)

    def pop_next(self,) -> 'CompilationFileNode':
        """ Pops the next node that should be compiled outside of the queue,
        and returns it. If the queue is empty, returns `None`. """

        try:
            return next(self._queue)
        except StopIteration:
            return None

    def generate(self, node: 'CompilationFileNode') -> 'NodeCompilationStatus':
        if self._status.get(node) is None:
            try:
                node.generate()

            except litemakeCompilationError:
                self._status[node] = NodeFailed
                temp = node
                while temp.parent is not None:
                    self._status[temp.parent] = NodeSkipped
                    temp = temp.parent

            else:
                self._status[node] = NodePassed

        return self._status[node]
