import typing
from glob import glob
from os import path

from .compiler import litemakeCompiler as Compiler
from litemake.printer import litemakePrinter as Printer
from litemake.exceptions import litemakeNoSourcesWarning


class TargetCompiler:

    def __init__(self,
                 sources: typing.List[str],  # list of globs
                 compiler: Compiler,
                 dependencies: typing.List['TargetCompiler'],
                 dependency: bool,  # is this target a dependency of another
                 ) -> None:
        self.sources = sources
        self.compiler = compiler
        self.dependencies = dependencies
        self.dependency = dependency

    def compile(self) -> typing.List[str]:
        """ Compiles all object files required for this target, and return
        a list of paths to those object files. """

        # TODO: compile each dependency as a static library
        return self.compile_me() + self.compile_dependencies()

    def compile_me(self) -> typing.List[str]:
        """ Compiles only object file that are direct sources of this target
        (without dependencies). Returns a list of paths to all compiled object
        files. """

        files = list(self.find_sources())
        # TODO: add a warning if no sources found in target.

        for file in files:
            self.compiler.compile_file(file)

        return [
            self.compiler.src_to_obj_path(src)
            for src in files
        ]

    def compile_dependencies(self) -> typing.List[str]:
        """ Compile all object files of dependencies for this target, and
        return a list of path to those object files. """

        objs = list()
        for target in self.dependencies:
            objs += target.compile()

        return objs

    def find_sources(self) -> typing.List[str]:
        """ Converts the list of globs into a list of file path that matches
        the globs pattern. """

        yield from (
            file
            for glb in self.sources
            for file in glob(glb, recursive=True)
            if path.isfile(file)
        )
