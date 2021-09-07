''' /parse/endpoints.py - litemake - Alon Krymgand Osovsky (2021) '''

import typing
from os import path


from litemake.exceptions import litemakeTemplateError

from .templates import (
    BaseTemplate,
    TemplateEndpoint,
    MISSING,
)


class StringTemplate(TemplateEndpoint):

    def __init__(self,
                 min_len: int = None,
                 max_len: int = None,
                 allowed_chars: str = None,
                 no_repeating: str = None,
                 no_on_edges: str = None,
                 default=MISSING,
                 ) -> None:
        super().__init__(default)
        self.min_len = min_len
        self.max_len = max_len
        self.allowed_chars = allowed_chars
        self.no_repeating = no_repeating
        self.no_on_edges = no_on_edges

    def validate(self, value, fieldpath: typing.List[str]) -> str:
        if not self.required and value is MISSING:
            return self.default

        # validate type str
        super().validate(value, fieldpath)
        self.assert_type(value, str, fieldpath)

        # validate string length
        if self.max_len is not None and self.max_len < len(value):
            raise litemakeTemplateError(
                fieldpath, f'Max length allowed is {self.max_len!r} (not {len(value)})'
            )

        if self.min_len is not None and self.min_len > len(value):
            raise litemakeTemplateError(
                fieldpath, f'Min length required is {self.min_len!r} (not {len(value)})'
            )

        # validate chars
        if self.allowed_chars is not None:
            for c in value:
                if c not in self.allowed_chars:
                    raise litemakeTemplateError(
                        fieldpath, f'Character {c!r} is not allowed')

        # validate no repeating chars
        if self.no_repeating is not None:
            if len(value) >= 2:
                for c, cc in zip(value[1:], value[:-1]):
                    if c in self.no_repeating and cc in self.no_repeating:
                        raise litemakeTemplateError(
                            fieldpath,
                            f"Character {c!r} can't be followed by {c!r}"
                        )

        # validate edges
        if self.no_on_edges is not None:
            if value[0] in self.no_on_edges:
                raise litemakeTemplateError(
                    fieldpath, f"Character {value[0]!r} isn't allowed as a starting character")
            if value[-1] in self.no_on_edges:
                raise litemakeTemplateError(
                    fieldpath, f"Character {value[-1]!r} isn't allowed as an ending character")

        return value


class FolderPathTemplate(StringTemplate):

    def __init__(self, default=MISSING):
        super().__init__(min_len=1, default=default)

    def validate(self, value, fieldpath: typing.List[str]):
        if not self.required and value is MISSING:
            return self.default

        super().validate(value, fieldpath)

        if path.isfile(value):
            raise litemakeTemplateError(
                fieldpath, f"File named {value!r} already exists")

        return value


class RelFolderPathTemplate(FolderPathTemplate):

    def __init__(self, default=MISSING) -> None:
        super().__init__(default=default)

    def validate(self, value, fieldpath: typing.List[str]):
        if not self.required and value is MISSING:
            return self.default

        super().validate(value, fieldpath)

        if path.isabs(value):
            raise litemakeTemplateError(
                fieldpath, f"Path must be relative, not absolute ({value!r})")

        return value


class IntegerTemplate(TemplateEndpoint):

    def __init__(self,
                 range_min: int = None,
                 range_max: int = None,
                 default=MISSING,
                 ) -> None:
        super().__init__(default)
        self.range_min = range_min
        self.range_max = range_max

    def validate(self, value, fieldpath: typing.List[str]):
        if not self.required and value is MISSING:
            return self.default

        super().validate(value, fieldpath)
        self.assert_type(value, int, fieldpath)

        if self.range_min is not None:
            if value < self.range_min:
                raise litemakeTemplateError(
                    fieldpath, f'Min value allowed is {self.range_min!r}')

        if self.range_max is not None:
            if value > self.range_max:
                raise litemakeTemplateError(
                    fieldpath, f'Max value allowed is {self.range_max!r}')

        return value


class BoolTemplate(TemplateEndpoint):

    def validate(self, value, fieldpath: typing.List[str]):
        if not self.required and value is MISSING:
            return self.default

        super().validate(value, fieldpath)
        self.assert_type(value, bool, fieldpath)
        return value


class ListTemplate(TemplateEndpoint):

    def __init__(self,
                 listof: BaseTemplate,
                 min_len: int = None,
                 max_len: int = None,
                 default=MISSING,
                 ) -> None:
        super().__init__(default)
        self.listof = listof
        self.min_len = min_len
        self.max_len = max_len

    def validate(self, value, fieldpath: typing.List[str]):
        if not self.required and value is MISSING:
            return self.default

        super().validate(value, fieldpath)
        self.assert_type(value, list, fieldpath)

        if self.min_len is not None:
            if len(value) < self.min_len:
                raise litemakeTemplateError(
                    fieldpath,
                    f'Min {self.min_len!r} item(s) required')

        if self.max_len is not None:
            if len(value) > self.max_len:
                raise litemakeTemplateError(
                    fieldpath,
                    f'Max {self.max_len!r} item(s) allowed')

        new = list()
        for index, item in enumerate(value):
            new.append(
                self.listof.validate(item, fieldpath + [index])
            )

        return new


class DictTemplate(TemplateEndpoint):

    def __init__(self,
                 keys: TemplateEndpoint,
                 values: BaseTemplate,
                 min_len: int = None,
                 max_len: int = None,
                 default=MISSING,
                 ) -> None:
        super().__init__(default)
        self.keys = keys
        self.values = values

        # TODO: Combine all templates with 'min, max length' settings
        #       into a single class that others can inherit from.
        self.min_len = min_len
        self.max_len = max_len

    def validate(self, value, fieldpath: typing.List[str]):
        if not self.required and value is MISSING:
            return self.default

        super().validate(value, fieldpath)
        self.assert_type(value, dict, fieldpath)

        if self.min_len is not None:
            if len(value) < self.min_len:
                raise litemakeTemplateError(
                    fieldpath,
                    f'Min {self.min_len!r} item(s) required')

        if self.max_len is not None:
            if len(value) > self.max_len:
                raise litemakeTemplateError(
                    fieldpath,
                    f'Max {self.max_len!r} item(s) allowed')

        new = dict()
        for key, item in value.items():
            new_key = self.keys.validate(key, fieldpath)
            new_val = self.values.validate(item, fieldpath + [key])
            new[new_key] = new_val

        return new
