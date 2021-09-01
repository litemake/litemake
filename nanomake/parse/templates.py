''' /parse/templates.py - nanomake - Alon Krymgand Osovsky (2021) '''

import re
import os.path
from abc import ABC, abstractmethod


class SetupArgTemplate(ABC):

    def __init__(self, default=None, required=False):
        self.default = default
        self.required = required

    @abstractmethod
    def validate(self, value):
        ''' An abstract method that will receive a value, and will validate it.
        The validation proccess can throw an error if the value is completely
        irrelevant, or change it and return the new value. '''

    @staticmethod
    def assert_type(value, type) -> None:
        ''' A helper method that receives a value and type, and raises an
        assertion error if the given value doesn't match the given type. '''

        # Generate strings of class names
        required_name = type.__name__
        value_type_name = value.__class__.__name__

        # Construct error message
        required = f'Expected type {required_name!r}'
        notwhat = f'not {value_type_name!r} ({value!r})'

        # Assert type, throw message if assertion fails
        assert isinstance(value, type), f'{required}, {notwhat}'


class SetupStringArg(SetupArgTemplate):

    def __init__(self,
                 min_len: int = None,
                 max_len: int = None,
                 allowed_chars: str = None,
                 no_repeating: str = None,
                 no_on_edges: str = None,
                 default=None,
                 required=False
                 ) -> None:
        super().__init__(default=default, required=required)
        self.min_len = min_len
        self.max_len = max_len
        self.allowed_chars = allowed_chars
        self.no_repeating = no_repeating
        self.no_on_edges = no_on_edges

    def validate(self, value) -> str:

        # validate type str
        self.assert_type(value, str)

        # validate string length
        if self.min_len is not None:
            assert self.min_len <= len(
                value), f'Minimum length required is {self.min_len!r}'

        if self.max_len is not None:
            assert self.max_len >= len(
                value), f'Maximum length required is {self.max_len!r}'

        # validate chars
        if self.allowed_chars is not None:
            for c in value:
                assert c in self.allowed_chars, f'Character {c!r} is not allowed'

        # validate no repeating chars
        print(f'{self.no_repeating=}')
        if self.no_repeating is not None:
            if len(value) >= 2:
                for c, cc in zip(value[1:], value[:-1]):
                    if c in self.no_repeating and cc in self.no_repeating:
                        raise AssertionError(
                            f"Character {c!r} can't be followed by {c!r}")

        # validate edges
        if self.no_on_edges is not None:
            assert value[0] not in self.no_on_edges, (
                f"Character {value[0]!r} isn't allowed as a starting character")
            assert value[-1] not in self.no_on_edges, (
                f"Character {value[-1]!r} isn't allowed as an ending character")

        return value


class SetupFolderPathArg(SetupArgTemplate):

    def validate(self, value):
        self.assert_type(value, str)
        assert os.path.isfile(value), f"A file named {value!r} already exists"
        return os.path.abspath(value)


class SetupIntegerArg(SetupArgTemplate):

    def __init__(self,
                 range_min: int = None,
                 range_max: int = None,
                 default=None,
                 required=False,
                 ) -> None:
        super().__init__(default=default, required=required)
        self.range_min = range_min
        self.range_max = range_max

    def validate(self, value):
        self.assert_type(value, int)
        assert value >= self.range_min, f"Minimum value is {self.range_min!r}"
        assert value <= self.range_max, f"Maximum value is {self.range_max!r}"
        return value
