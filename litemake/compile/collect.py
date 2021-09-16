import typing

from .target import TargetCompiler
from .output import OutputFolder

if typing.TYPE_CHECKING:
    from .compilers import AbstractCompiler
    from .graph import CompilationFileNode


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
