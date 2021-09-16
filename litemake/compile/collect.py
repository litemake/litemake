import typing

from .target import TargetCompiler
from .output import OutputFolder

from litemake.printer import litemakePrinter as Printer
from .graph import (
    ObjectFileNode,
    ArchiveFileNode,
    ExecutableFileNode,
)

if typing.TYPE_CHECKING:
    from .compilers import AbstractCompiler
    from .graph import CompilationFileNode


def type_filter(instances, filter: type) -> tuple:
    return tuple(
        i for i in instances
        if isinstance(i, filter)
    )


class TargetsCollection:

    def __init__(self,
                 package: str,
                 version: typing.Tuple[int, int, int],
                 basepath: str,
                 outpath: str,
                 compiler: 'AbstractCompiler',
                 ) -> None:
        self.package = package
        self.version = version
        self.basepath = basepath
        self.outpath = outpath
        self.compiler = compiler
        self.targets = list()

    def collect(self,
                target: str,
                library: bool,
                sources: typing.List[str],
                ) -> None:
        self.targets.append(
            TargetCompiler(
                package=self.package,
                target=target,
                version=self.version,
                isexec=not library,
                basepath=self.basepath,
                sources=sources,
                compiler=self.compiler,
            )
        )

    def make(self) -> None:
        out = OutputFolder(self.outpath)
        generated: typing.List['CompilationFileNode'] = list()

        for target in self.targets:
            target: TargetCompiler
            graph = target.build_graph(out)
            generated += graph.generate_all()

        self._print_generated_summary(generated)

    @staticmethod
    def _print_generated_summary(
            generated: typing.List['CompilationFileNode']) -> None:

        if not generated:
            Printer.summary(
                '*summary:* everything up-to-date! (no files generated)')

        else:

            # print a list of generated file paths, if debug verbose enabled.

            debug = (
                f'*{index}:* {node.dest}'
                for index, node in enumerate(generated, start=1)
            )

            Printer.debug('\n'.join((
                '*all generated files, in order of generation:*',
                *debug,
            )))

            # print a short summary and count generated objects, archives,
            # and executables.

            filters = {
                'object(s)': ObjectFileNode,
                'archive(s)': ArchiveFileNode,
                'executable(s)': ExecutableFileNode,
            }

            filtered_nodes = {
                name: type_filter(generated, cls)
                for name, cls in filters.items()
            }

            summary = (
                f'*{len(nodes)}* {name}'
                for name, nodes in filtered_nodes.items()
                if len(nodes) != 0
            )

            Printer.summary('\n'.join((
                f'*summary:* generated *{len(generated)!r}* file(s):',
                *summary,
            )))
