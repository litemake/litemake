import typing

from .target import TargetCompiler

if typing.TYPE_CHECKING:
    from .compilers import AbstractCompiler


class TargetsCollection:

    def __init__(self,
                 package: str,
                 version: typing.Tuple[int, int, int],
                 basepath: str,
                 compiler: 'AbstractCompiler',
                 ) -> None:
        self.package = package
        self.version = version
        self.basepath = basepath
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
