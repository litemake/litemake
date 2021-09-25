import typing

import os
import sys

from litemake.folders import ProjectFolder
from litemake.compile import NodesCollector


def make(*targets: typing.Tuple[str]):
    project = ProjectFolder(os.getcwd())
    graphs = project.collect(*targets)

    for graph in graphs:
        for node in NodesCollector(graph).outdated_nodes():
            node.generate()


def main():
    args = sys.argv[1:]
    make(*args)


if __name__ == '__main__':
    main()
