import typing

import os
import sys

from litemake.folders import ProjectFolder


def make(*targets: typing.Tuple[str]):
    project = ProjectFolder(os.getcwd())
    graphs = project.collect(*targets)


def main():
    args = sys.argv[1:]
    make(*args)


if __name__ == '__main__':
    main()
