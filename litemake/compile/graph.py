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
    def generate(self,) -> None:
        """ A method that generates (compiles) the current node only.
        It assumes that the dependencies are already generated. """

    @property
    def outdated(self,) -> bool:
        return not os.path.exists(self.dest)

    @property
    @abstractmethod
    def outdated_subtree(self,) -> bool:
        """ True at least one node in the subtree that this node is the head
        node in is outdated, or if this node is outdated. """

    @abstractmethod
    def all_nodes(self,) -> typing.Generator['CompilationFileNode', None, None]:
        """ Generator that yields all nodes in the sub-tree in which the current
        node is the head node. Nodes are yielded in order of dependence. """


class ObjectFileNode(CompilationFileNode):
    """ A node that represents a source file that is compiled into an object
    file. """

    def __init__(self,
                 src: str,
                 dest: str,
                 compiler: AbstractCompiler,
                 includes: typing.List[str],
                 parent: 'ArchiveFileNode',
                 ) -> None:
        super().__init__(dest, compiler, parent)
        self.src = src
        self.includes = includes

    def generate(self,) -> None:
        os.makedirs(os.path.dirname(self.dest), exist_ok=True)
        self.compiler.create_obj(self.src, self.dest, self.includes)

    @property
    def outdated(self,) -> bool:
        return (super().outdated or
                os.path.getmtime(self.src) > os.path.getmtime(self.dest))

    @property
    def outdated_subtree(self,) -> bool:
        return self.outdated

    def all_nodes(self,) -> typing.Generator['CompilationFileNode', None, None]:
        # There are no nodes that are dependent on an object file, and thus
        # this generator only yields the current node.
        yield self


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

    @property
    def is_empty(self) -> bool:
        """ Returns True if there are no object or archives inside this archive. """
        return not set().union(self.dep_objects, self.dep_archives)

    def add_object(self, node: 'ObjectFileNode') -> None:
        good = node not in self.dep_objects
        if good: self.dep_objects.add(node)  # noqa: E701
        return good

    def generate(self,) -> None:
        os.makedirs(os.path.dirname(self.dest), exist_ok=True)
        objs = [obj.dest for obj in self.dep_objects]
        self.compiler.create_archive(self.dest, objs)

    @property
    def outdated_subtree(self,) -> bool:
        return self.outdated or any(
            dep.outdated_subtree
            for dep in self.dep_archives.union(self.dep_objects)
        )

    def all_nodes(self,) -> typing.Generator['CompilationFileNode', None, None]:
        for dep in self.dep_archives:
            yield from dep.all_nodes()
        for obj in self.dep_objects:
            yield from obj.all_nodes()
        yield self


class ExecutableFileNode(ArchiveDependentFileNode):
    """ A node that represents an executable. In litemake, an executable can
    depend only on archives, and can't depend on standalone object files.
    The executable node is the head node, and thus it doesn't have a parent. """

    def __init__(self,
                 dest: str,
                 compiler: AbstractCompiler,
                 ) -> None:
        super().__init__(dest, compiler, parent=None)

    @property
    def is_empty(self,) -> bool:
        return all(a.is_empty for a in self.dep_archives)

    def generate(self,) -> None:
        os.makedirs(os.path.dirname(self.dest), exist_ok=True)
        deps = [arc.dest for arc in self.dep_archives]
        self.compiler.create_executable(self.dest, deps)

    @property
    def outdated_subtree(self,) -> bool:
        return self.outdated or any(
            dep.outdated_subtree
            for dep in self.dep_archives
        )

    def all_nodes(self,) -> typing.Generator['CompilationFileNode', None, None]:
        for dep in self.dep_archives:
            yield from dep.all_nodes()
        yield self
