import toml
from abc import ABC
from litemake.exceptions import litemakeParsingError, litemakeTemplateError

import typing
if typing.TYPE_CHECKING:
    from .templates import BaseTemplate  # pragma: no cover


class FileParser(ABC):
    """ An abstract file parser that loads a TOML file and validates its content
    with a given and pre-defined template. """

    @property
    @classmethod
    def TEMPLATE(cls) -> 'BaseTemplate':
        """ A Template that is being used to validate data in the file. """

    def __init__(self, filepath: str):
        self.__filepath = filepath

        # Load TOML file into Python objects
        try:
            with open(filepath, mode='r', encoding='utf8') as file:
                data = toml.load(file)

        # Raise a custom error if failed to parse TOML file
        except toml.TomlDecodeError as err:
            raise litemakeParsingError(
                filename=filepath,
                line=err.lineno,
                col=err.colno,
                msg=err.msg,
            ) from None

        # Validate loaded data
        try:
            self._data = self.TEMPLATE.validate(data, fieldpath=list())

        # Raise a custom configuration error if validation faileds
        except litemakeTemplateError as err:
            raise err.to_config_error(filepath)

    @property
    def filepath(self,) -> str:
        """ The path to the current configuration TOML file. """
        return self.__filepath
