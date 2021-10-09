import typing

from .base import AbstractCompiler
from .gnu import GccCompiler, GplusplusCompiler
from .llvm import ClangCompiler, ClangplusplusCompiler

COMPILERS = {
    compiler.name: compiler
    for compiler in {
        GccCompiler,
        GplusplusCompiler,
        ClangCompiler,
        ClangplusplusCompiler,
    }
}


def Compiler(name: str) -> typing.Optional[AbstractCompiler]:
    """Converts the given compiler name into an instance of the compiler
    class. If the given name isn't recognized, returns `None`."""
    return COMPILERS.get(name)()
