import os
import typing
from glob import glob

from .compilers import AbstractCompiler
from .output import litemakeOutputFolder as OutputFolder
from .graph import (
    CompilationFileNode,
    ObjectFileNode,
    ArchiveFileNode,
    ExecutableFileNode,
)


class TargetCompiler:

    def __init__(self,
                 package: str,
                 target: str,
                 version: typing.Tuple[int, int, int],
                 basepath: str,
                 sources: typing.List[str],  # list of globs
                 compiler: AbstractCompiler,
                 ) -> None:
        self.package = package
        self.target = target
        self.version = version
        self.basepath = basepath
        self.sources = sources
        self.compiler = compiler

    def build_executable_graph(self, output: OutputFolder) -> ExecutableFileNode:
        libid = output.library_id(self.package, self.target, self.version)
        dest = os.path.join(self.basepath, libid + '.out')

        executable = ExecutableFileNode(dest, self.compiler)

        archive = self.build_archive_graph(output)
        executable.add_dep_archive(archive)

        return executable

    def build_archive_graph(self, output: OutputFolder) -> ArchiveFileNode:
        archive = ArchiveFileNode(
            dest=output.archive_path(self.package, self.target, self.version),
            compiler=self.compiler,
        )

        for src in self.find_sources():
            dest = self.source_to_object(src, output)
            node = ObjectFileNode(
                src, dest,
                compiler=self.compiler, parent=archive)
            archive.add_object(node)

        return archive

    def source_to_object(self, src: str, output: OutputFolder) -> str:
        return output.object_path(self.package, self.target, self.version,
                                  os.path.relpath(src, self.basepath))

    def find_objects(self, output: OutputFolder) -> typing.Generator[str, None, None]:
        yield from (
            self.source_to_object(src, output)
            for src in self.find_sources()
        )

    def find_sources(self) -> typing.Generator[str, None, None]:
        """ Converts the list of globs into a list of file path that matches
        the globs pattern. """

        yield from (
            file
            for glb in self.sources
            for file in glob(
                os.path.join(self.basepath, glb), recursive=True)
            if os.path.isfile(file)
        )
