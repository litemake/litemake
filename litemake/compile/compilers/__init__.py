from .base import AbstractCompiler
from .gnu import GccCompiler, GplusplusCompiler
from .llvm import ClangCompiler

COMPILERS = {
    compiler.name(): compiler
    for compiler in
    {GccCompiler, GplusplusCompiler, ClangCompiler}
}

__all__ = [
    'AbstractCompiler', 'COMPILERS',
    'GccCompiler', 'GplusplusCompiler',
    'ClangCompiler',
]
