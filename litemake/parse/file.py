import toml
from abc import ABC, abstractclassmethod
from litemake.exceptions import (
    litemakeParsingError,
    litemakeTemplateError,
    litemakeFileNotFoundError,
)

import typing
if typing.TYPE_CHECKING:
    from .templates import BaseTemplate  # pragma: no cover


class FileParser(ABC):
    """ An abstract file parser that loads a TOML file and validates its content
    with a given and pre-defined template. """

    @property
    @abstractclassmethod
    def TEMPLATE(cls) -> 'BaseTemplate':
        """ A Template that is being used to validate data in the file. """

    def __load_toml_file(self, filepath: str) -> dict:
        # Load TOML file into Python objects
        try:
            with open(filepath, mode='r', encoding='utf8') as file:
                return toml.load(file)

        # Raise a custom error if failed to parse TOML file
        except toml.TomlDecodeError as err:
            raise litemakeParsingError(
                filename=filepath,
                line=err.lineno,
                col=err.colno,
                msg=err.msg,
            ) from None

        except FileNotFoundError:
            raise litemakeFileNotFoundError(filepath) from None

    def __validate_data(self, data: dict) -> dict:
        try:  # Validate loaded data
            return self.TEMPLATE.validate(data, fieldpath=list())

        except litemakeTemplateError as err:
            # Raise a custom configuration error if validation faileds
            raise err.to_config_error(self.filepath)

    def __init__(self, filepath: str):
        self.__filepath = filepath
        data = self.__load_toml_file(filepath)
        self._data = self.__validate_data(data)

    @property
    def filepath(self,) -> str:
        """ The path to the current configuration TOML file. """
        return self.__filepath
