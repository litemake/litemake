import typing
if typing.TYPE_CHECKING:
    from litemake.compile.graph import CompilationFileNode

import os
import sys

from litemake.folders import ProjectFolder
from litemake.compile import NodesCollector


def make(*targets: typing.Tuple[str]):
    project = ProjectFolder(os.getcwd())
    graphs = project.collect(*targets)

    for graph in graphs:
        collector = NodesCollector(graph)
        node = collector.pop_next()

        while node is not None:
            result = collector.generate(node)
            print(result.color + node.dest)
            node = collector.pop_next()


def main():
    args = sys.argv[1:]
    make(*args)


if __name__ == '__main__':
    main()
