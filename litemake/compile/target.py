import os
import typing
from glob import glob

from .compilers import AbstractCompiler
from .output import OutputFolder
from .graph import (
    ObjectFileNode,
    ArchiveFileNode,
    ExecutableFileNode,
)

if typing.TYPE_CHECKING:
    from .graph import CompilationFileNode  # pragma: no cover


class TargetCompiler:

    def __init__(self,
                 package: str,
                 target: str,
                 version: typing.Tuple[int, int, int],
                 isexec: bool,
                 basepath: str,
                 sources: typing.List[str],  # list of globs
                 includes: typing.List[str],  # list of paths to folders
                 compiler: AbstractCompiler,
                 ) -> None:
        self.package = package
        self.target = target
        self.version = version
        self.isexec = isexec
        self.basepath = basepath
        self.sources = sources
        self.includes = includes
        self.compiler = compiler

    def build_graph(self, output: OutputFolder) -> 'CompilationFileNode':
        if self.isexec:
            return self._build_executable_graph(output)
        else:
            return self._build_archive_graph(output)

    def _build_executable_graph(self, output: OutputFolder) -> ExecutableFileNode:
        name = output.binary_name(self.package, self.target, self.version)
        dest = os.path.join(self.basepath, name)
        executable = ExecutableFileNode(dest, self.compiler)

        archive = self._build_archive_graph(output)
        executable.add_dep_archive(archive)

        return executable

    def _build_archive_graph(self, output: OutputFolder) -> ArchiveFileNode:
        archive = ArchiveFileNode(
            dest=output.archive_path(self.package, self.target, self.version),
            compiler=self.compiler,
        )

        for src in self.find_sources():
            dest = self.source_to_object(src, output)
            node = ObjectFileNode(
                src, dest,
                compiler=self.compiler,
                includes=self.includes,
                parent=archive,
            )
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
