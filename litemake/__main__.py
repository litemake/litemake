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
        while (node := collector.pop_next()) is not None:
            node: 'CompilationFileNode'
            result = collector.generate(node)
            print(result.color + node.dest)


def main():
    args = sys.argv[1:]
    make(*args)


if __name__ == '__main__':
    main()
