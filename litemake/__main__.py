import typing
if typing.TYPE_CHECKING:
    from litemake.compile.graph import CompilationFileNode

import os
import sys

from litemake.folders import ProjectFolder
from litemake.compile import NodesCollector
from litemake.printer import DefaultProgressPrinter


def make(*targets: typing.Tuple[str]):
    project = ProjectFolder(os.getcwd())
    graphs = project.collect(*targets)

    for graph in graphs:
        collector = NodesCollector(graph)
        progress = DefaultProgressPrinter(
            collector.count_total, collector.count_outdated)
        while (node := collector.pop_next()) is not None:
            node: 'CompilationFileNode'
            result = collector.generate(node)
            progress.register_status(node, result)
            print(progress)

def main():
    args = sys.argv[1:]
    make(*args)


if __name__ == '__main__':
    main()
