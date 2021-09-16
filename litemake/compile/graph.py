import typing
import os
from abc import ABC, abstractmethod
from .compilers import AbstractCompiler


class CompilationFileNode(ABC):

    def __init__(self,
                 dest: str,
                 compiler: AbstractCompiler,
                 parent: typing.Optional['CompilationFileNode'],
                 ) -> None:
        self.dest = dest
        self.compiler = compiler
        self.parent = parent

    def set_parent(self, parent: 'CompilationFileNode') -> None:
        self.parent = parent

    @abstractmethod
    def generate_myself(self,) -> None:
        """ A method that generates (compiles) the current node only.
        It assumes that the dependencies are already generated. """

    @abstractmethod
    def generate_all(self,) -> typing.List['CompilationFileNode']:
        """ A method that generates the subtree of the node (generates
        dependencies first, and only then regenerates this).
        This method also checks if the regeneration is required using the
        'required_regen' property, and skips regeneration of up to date
        dependencies. Returns a list of all nodes that were regenerated. """

    @property
    def required_regen(self,) -> bool:
        return not os.path.exists(self.dest)


class ObjectFileNode(CompilationFileNode):
    """ A node that represents a source file that is compiled into an object
    file. """

    def __init__(self,
                 src: str,
                 dest: str,
                 compiler: AbstractCompiler,
                 parent: 'ArchiveFileNode',
                 ) -> None:
        super().__init__(dest, compiler, parent)
        self.src = src

    def generate_myself(self,) -> None:
        self.compiler.create_obj(self.src, self.dest)

    def generate_all(self) -> typing.List['CompilationFileNode']:
        if self.required_regen:
            self.generate_myself()  # noqa: E701
            return [self]
        return list()

    @property
    def required_regen(self,) -> bool:
        return (super().required_regen or
                os.path.getmtime(self.src) > os.path.getmtime(self.dest))


class ArchiveDependentFileNode(CompilationFileNode):

    def __init__(self,
                 dest: str,
                 compiler: AbstractCompiler,
                 parent,
                 ) -> None:
        super().__init__(dest, compiler, parent)
        self.dep_archives: typing.Set['ArchiveFileNode'] = set()

    def add_dep_archive(self, node: 'ArchiveFileNode') -> None:
        good = node not in self.dep_archives
        if good: self.dep_archives.add(node)  # noqa: E701
        return good


class ArchiveFileNode(ArchiveDependentFileNode):
    """ A node that represents an archive (collection) of multiple object
    files. """

    def __init__(self,
                 dest: str,
                 compiler: AbstractCompiler,
                 parent: 'ExecutableFileNode' = None,
                 ) -> None:
        super().__init__(dest, compiler, parent=parent)
        self.dep_objects: typing.Set['ObjectFileNode'] = set()

    def add_object(self, node: 'ObjectFileNode') -> None:
        good = node not in self.dep_objects
        if good: self.dep_objects.add(node)  # noqa: E701
        return good

    def generate_all(self,) -> typing.List['CompilationFileNode']:
        generated = list()

        for arc in self.dep_archives:
            generated += arc.generate_all()

        for obj in self.dep_objects:
            generated += obj.generate_all()

        if generated or self.required_regen:
            self.generate_myself()
            generated.append(self)

        return generated

    def generate_myself(self,) -> None:
        objs = [obj.dest for obj in self.dep_objects]
        self.compiler.create_archive(self.dest, objs)


class ExecutableFileNode(ArchiveDependentFileNode):
    """ A node that represents an executable. In litemake, an executable can
    depend only on archives, and can't depend on standalone object files.
    The executable node is the head node, and thus it doesn't have a parent. """

    def __init__(self,
                 dest: str,
                 compiler: AbstractCompiler,
                 ) -> None:
        super().__init__(dest, compiler, parent=None)

    def generate_all(self,) -> typing.List['CompilationFileNode']:
        generated = list()

        for arc in self.dep_archives:
            generated += arc.generate_all()

        if generated or self.required_regen:
            self.generate_myself()
            generated.append(self)

        return generated

    def generate_myself(self,) -> None:
        deps = [arc.dest for arc in self.dep_archives]
        self.compiler.create_executable(self.dest, deps)
