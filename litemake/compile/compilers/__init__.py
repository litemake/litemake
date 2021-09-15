from .base import AbstractCompiler
from .gnu import GccCompiler, GplusplusCompiler
from .llvm import ClangCompiler, ClangplusplusCompiler

COMPILERS = {
    compiler.name: compiler
    for compiler in
    {GccCompiler, GplusplusCompiler, ClangCompiler, ClangplusplusCompiler}
}

__all__ = [
    'AbstractCompiler', 'COMPILERS',
    'GccCompiler', 'GplusplusCompiler',
    'ClangCompiler', 'ClangplusplusCompiler'
]
