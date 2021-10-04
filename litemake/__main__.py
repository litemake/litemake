import typing

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

        node = collector.pop_next()
        while node is not None:
            status = collector.generate(node)
            progress.register_status(node, status)
            node = collector.pop_next()
            print(progress)


def main():
    args = sys.argv[1:]
    make(*args)


if __name__ == '__main__':
    main()
