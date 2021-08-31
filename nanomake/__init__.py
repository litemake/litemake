''' nanomake - Alon Krymgand Osovsky (2021) '''

__version__ = '0.1.0'
__description__ = 'A new way to build, test and distribute your C/C++ projects and libraries.'
__nanomake_spec__ = 1

__all__ = [
    'main',
    'NanomakePrinter',
]

from .nanomake import main
from .printer import NanomakePrinter
