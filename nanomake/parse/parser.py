import string

import toml
from toml import TomlDecodeError

from .types import (
    SetupStringArg as String,
    SetupFolderPathArg as FolderPath,
    SetupIntegerArg as Integer,
)

from nanomake.exceptions import (
    NanomakeParsingError,
    NanomakeSetupFileNotFoundError,
)


class SetupConfigParser:

    NAME_CHARS = string.ascii_letters + string.digits + '-_.'
    SPECIAL_CHARS = '-_.'

    TEMPLATE = {
        'nanomake': {
            'spec': Integer(range_min=0, default=0),
            'output': FolderPath(default='./build/'),
            'compiler': String(default='g++'),
            'objext': String(default='{relativeOutputFolder}/{baseFileName}.o'),

            'meta': {
                'name': String(
                    required=True,
                    min_len=3, max_len=30,
                    allowed_chars=NAME_CHARS,
                    no_repeating=SPECIAL_CHARS, no_on_edges=SPECIAL_CHARS),

                'description': String(max_len=200),
                'author': String(max_len=200),
                # TODO: add metadata fields: email, url(s)

                'version': {
                    'major': Integer(range_min=0, default=0),
                    'minor': Integer(range_min=0, default=0),
                    'patch': Integer(range_min=0, default=0),
                    'label': String(
                        max_len=10, allowed_chars=NAME_CHARS,
                        no_repeating=SPECIAL_CHARS,
                        no_on_edges=SPECIAL_CHARS),
                },

                'standard': String(default=''),
                # TODO: option to specify a list of supported standards

            }
        }
    }

    def __init__(self, filepath: str):
        try:
            with open(filepath, mode='r', encoding='utf8') as file:
                self.raw = toml.load(file)

        except FileNotFoundError:
            raise NanomakeSetupFileNotFoundError(filepath) from None

        except TomlDecodeError as err:
            raise NanomakeParsingError(
                filename=filepath,
                line=err.lineno,
                col=err.colno,
                msg=err.msg,
            ) from None
