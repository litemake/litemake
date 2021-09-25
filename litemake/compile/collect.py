import typing
if typing.TYPE_CHECKING:
    from .graph import CompilationFileNode

from functools import cached_property


class NodesCollector:

    def __init__(self, tree: 'CompilationFileNode') -> None:
        self.nodes = list(tree.all_nodes())
        self.next_node_index = 0

    @property
    def count(self,) -> int:
        """ The number of nodes in the whole tree. """
        return len(self.nodes)

    @cached_property
    def count_outdated(self,) -> int:
        """ The number of nodes in the tree that needs to be regenerated. """
        return sum(node.outdated_subtree for node in self.nodes)

    def outdated_nodes(self,) -> typing.List['CompilationFileNode']:
        return [
            node
            for node in self.nodes
            if node.outdated_subtree
        ]
