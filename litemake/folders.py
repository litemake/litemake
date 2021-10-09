import os
from abc import ABC
from glob import glob

from litemake.constants import (
    TARGETS_CONFIG_FILENAME,
    SETTINGS_FILENAME,
)

from litemake.parse import (
    TargetsParser,
    SettingsParser,
)

from litemake.compile.graph import (
    ExecutableFileNode,
    ArchiveFileNode,
    ObjectFileNode,
)
from litemake.exceptions import litemakeUnknownTargetsError

import typing

if typing.TYPE_CHECKING:
    from litemake.parse.targets import TargetInfo
    from litemake.compile.graph import CompilationFileNode


class Folder(ABC):
    """A base class that easily represents a special folder in litemake."""

    def __init__(self, basepath: str) -> None:
        self.__basepath = basepath

    @property
    def basepath(
        self,
    ) -> str:
        return self.__basepath

    def join(self, *args: str) -> str:
        return os.path.join(self.basepath, *args)


class OutputFolder(Folder):
    """Represents the folder that litemake caches it's data in."""

    @property
    def archives(
        self,
    ) -> str:
        return self.join("archives")

    @property
    def objects(
        self,
    ) -> str:
        return self.join("objects")

    def archive_name(self, target: "TargetInfo") -> str:
        return os.path.join(self.archives, f"{target.name}.a")

    def object_name(self, target: "TargetInfo", relative: str) -> str:
        folder = os.path.join(self.objects, target.name)
        return os.path.join(folder, relative)


class ProjectFolder(Folder):
    """Represents the base folder of the user application code.
    This folder should contain all configuration files that are needed for
    litemake to run."""

    def __init__(
        self,
        basepath: str,
    ) -> None:
        super().__init__(basepath)

        targets_path = self.join(TARGETS_CONFIG_FILENAME)
        settings_path = self.join(SETTINGS_FILENAME)

        self.targets = TargetsParser(targets_path)
        self.settings = SettingsParser(settings_path)
        # TODO: make the settings file not mandatory

        self.output = OutputFolder(self.settings.output)

    def collect(
        self, *targets: typing.Tuple[str]
    ) -> typing.List["CompilationFileNode"]:
        """Collect all files that are needed to generate the given targets."""

        # If no targets are provided, select default target
        if not targets:
            targets = (self.targets.default_target,)

        # Checking if unknown targets are provided
        known = self.targets.targets
        unknown = set(targets) - set(known)

        # If unknown targets provided, raise an error
        if unknown:
            raise litemakeUnknownTargetsError(unknown)

        # Build compilation graphs for all targets
        graphs = list()
        for name in targets:
            info = self.targets.target(name)
            graphs.append(self._build_compilation_graph(info))

        return graphs

    def _build_compilation_graph(self, target: "TargetInfo") -> "CompilationFileNode":
        """Converts the target information info a graph that represents the
        relashionships between source files, object files, archives, and
        executables in the program."""

        compiler = self.settings.compiler()

        # Each litemake target is compiled into an archive, and thus it is the
        # first instance that we create.
        archive = ArchiveFileNode(
            dest=self.output.archive_name(target),
            compiler=compiler,
        )

        # Now, its time to collect all needed source files
        sources = list()
        for glb in target.sources:
            if not os.path.isabs(glb):
                # if relative glob
                # TODO: all globs should be relative
                glb = os.path.join(self.settings.home, glb)

            sources += [
                g for g in sorted(glob(glb, recursive=True)) if os.path.isfile(g)
            ]

        # Now that all source files are collected, we create instances
        # of object files that they will be compiled to!
        for source in sources:
            rel = os.path.relpath(source, self.settings.home)
            obj = ObjectFileNode(
                src=source,
                dest=self.output.object_name(target, rel),
                compiler=compiler,
                includes=target.include,
                parent=archive,
            )
            archive.add_object(obj)

        if target.library:
            return archive

        else:
            # If the current target represnets an executable, we create it
            # too and return it instead of the archive.
            exe = ExecutableFileNode(
                dest=os.path.join(os.getcwd(), target.name),
                compiler=compiler,
            )
            archive.set_parent(exe)
            exe.add_dep_archive(archive)
            return exe
