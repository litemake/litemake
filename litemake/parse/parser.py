import typing
import string

import toml
from toml import TomlDecodeError

from .templates import Template

from .endpoints import (
    StringTemplate as String,
    CompilerTemplate as Compiler,
    FolderPathTemplate as FolderPath,
    RelFolderPathTemplate as RelFolderPath,
    IntegerTemplate as Integer,
    BoolTemplate as Bool,
    ListTemplate as ListOf,
    DictTemplate as Dict,
)

from litemake.exceptions import (
    litemakeParsingError,
    litemakeSetupFileNotFoundError,
    litemakeTemplateError,
)


class SetupConfigParser:

    SPECIAL_CHARS = '-_.'
    NAME_CHARS = string.ascii_letters + string.digits + SPECIAL_CHARS

    TEMPLATE = Template(
        litemake=Template(
            spec=Integer(range_min=0, default=0),
            output=FolderPath(default='./.litemake/'),
            compiler=Compiler(default='g++'),

            meta=Template(
                name=String(
                    min_len=3, max_len=30,
                    allowed_chars=NAME_CHARS,
                    no_repeating=SPECIAL_CHARS,
                    no_on_edges=SPECIAL_CHARS,
                ),

                description=String(max_len=200, default=str()),
                author=String(max_len=200, default=str()),
                # TODO: add metadata fields: email, url(s)

                version=Template(
                    major=Integer(range_min=0, default=0),
                    minor=Integer(range_min=0, default=0),
                    patch=Integer(range_min=0, default=0),
                    label=String(
                        default='', max_len=10,
                        allowed_chars=NAME_CHARS,
                        no_repeating=SPECIAL_CHARS,
                        no_on_edges=SPECIAL_CHARS,
                    ),
                ),

                standard=String(min_len=1),
                # TODO: a list of supported standards.
            ),
        ),

        # TODO: custom error message when no targets provided
        target=Dict(
            default=dict(),
            min_len=1,
            keys=String(
                min_len=1, max_len=30,
                allowed_chars=NAME_CHARS,
                no_repeating=SPECIAL_CHARS,
                no_on_edges=SPECIAL_CHARS,
            ),
            values=Template(
                library=Bool(default=False),
                sources=ListOf(
                    default=list(),
                    listof=String(min_len=1),
                ),
                include=ListOf(
                    default=list(),
                    listof=RelFolderPath(must_exist=True),
                ),
            ),
        ),
    )

    def __init__(self, filepath: str):
        self.filepath = filepath

        try:
            with open(filepath, mode='r', encoding='utf8') as file:
                self.raw = toml.load(file)

        except FileNotFoundError:
            raise litemakeSetupFileNotFoundError(filepath) from None

        except TomlDecodeError as err:
            raise litemakeParsingError(
                filename=filepath,
                line=err.lineno,
                col=err.colno,
                msg=err.msg,
            ) from None

        try:
            self.config = self.TEMPLATE.validate(self.raw, fieldpath=list())

        except litemakeTemplateError as err:
            raise err.to_config_error(filepath)
