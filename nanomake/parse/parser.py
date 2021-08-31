import typing
import string

import toml
from toml import TomlDecodeError

from .types import (
    SetupArgTemplate,
    SetupStringArg as String,
    SetupFolderPathArg as FolderPath,
    SetupIntegerArg as Integer,
)

from nanomake.exceptions import (
    NanomakeParsingError,
    NanomakeSetupFileNotFoundError,
    NanomakeConfigError,
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
        self.filepath = filepath

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

        self.config = self.validate(
            raw=self.raw,
            template=self.TEMPLATE,
            path=list(),
        )

    def validate(self, raw, template, path: typing.List[str]):
        if template is None:
            # RECURSIVE BASECASE:
            # If there is no template to validate,
            # we got to this point by the user that used an invalid
            # field, and thus we will raise an error.
            raise NanomakeConfigError(
                self.filepath, path, msg='Unknown field')

        if isinstance(template, SetupArgTemplate):
            # RECURSIVE BASECASE:
            # if the template is an instance of 'SetupArgTemplate',
            # we want to actually check the data in the field.

            if raw is None and template.required:
                # If the data isn't provided by the user but required,
                # we will raise an error
                raise NanomakeConfigError(
                    self.filepath, path, msg='Missing required field')

            elif raw is None and not template.required:
                # If however, the data is not required and not provided
                # by the user, we will return the default value.
                return template.default

            else:
                # If the user provided some data in this field,
                # we will need to validate the given data using
                # the 'validate' method of the 'SetupArgTemplate' class

                try:
                    return template.validate(raw)

                except AssertionError as err:
                    # The 'SetupArgTemplate' class uses assertions to validate
                    # data. If an assertion statemant fails, the data doesn't
                    # follow the template and we need to raise an error.
                    raise NanomakeConfigError(
                        self.filepath, path, ' '.join(err.args))

        if isinstance(template, dict):
            # RECURSIVE CALL
            # if the template is a dictionary, we haven't reached the recursive
            # base case yet. we will want to validate all items inside the dict.

            if raw is None:
                # if the user didn't provide his own data, we will assume
                # that an empty dict is provided. This is implemented to allow
                # default values inside dictionaries to be applied.
                raw = dict()

            if not isinstance(raw, dict):
                # If the template is a dict, the user must provide a dic too.
                # if the raw instance isn't a dict, we will raise an error!
                raise NanomakeConfigError(
                    self.filepath, path, 'Unexpected field')

            # We will get to this point if both the template and the raw data
            # are dictionaries. In this case, we will want to check the keys of
            # both the template (to check if the user missed some fields), and
            # the keys of the raw data (to check if the user provied unexpected
            # fields).

            raw_keys = set(raw.keys())
            temp_keys = set(template.keys())
            data = dict()

            for key in raw_keys.union(temp_keys):
                data[key] = self.validate(
                    raw=raw.get(key),
                    template=template.get(key),
                    path=path + [key],
                )

            return data
