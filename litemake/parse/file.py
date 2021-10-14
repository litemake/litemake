import toml
from abc import ABC, abstractclassmethod
from litemake.exceptions import (
    litemakeParsingError,
    litemakeTemplateError,
    litemakeConfigError,
    litemakeFileNotFoundError,
)

import typing

if typing.TYPE_CHECKING:
    from .templates import BaseTemplate  # pragma: no cover


class FileParser(ABC):
    """An abstract file parser that loads a TOML file and validates its content
    with a given and pre-defined template."""

    @property
    @abstractclassmethod
    def TEMPLATE(cls) -> "BaseTemplate":
        """A Template that is being used to validate data in the file."""

    def _load_toml_file(self, filepath: str) -> dict:
        # Load TOML file into Python objects
        try:
            with open(filepath, mode="r", encoding="utf8") as file:
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

    def _validate_data(self, data: dict) -> dict:
        try:  # Validate loaded data
            return self.TEMPLATE.validate(data, fieldpath=list())

        except litemakeTemplateError as err:
            # Raise a custom configuration error if validation fails
            raise litemakeConfigError.from_template_error(self.filepath, err)

    def __init__(self, filepath: str):
        self._filepath = filepath
        raw = self._load_toml_file(filepath)
        self._data = self._validate_data(raw)

    @property
    def filepath(
        self,
    ) -> str:
        """The path to the current configuration TOML file."""
        return self._filepath


class OptionalFileParser(FileParser):
    """An abstract file parser that loads a TOML file and validates its content
    with a given and pre-defined template. If it tries to load a files that
    doesn't exist, doesn't raise an error and loads the default configuration
    from the template."""

    def _load_toml_file(self, filepath: str) -> dict:
        try:
            return super()._load_toml_file(filepath)

        except litemakeFileNotFoundError:
            # If the file doesn't exist, loads an empty dict as the data.
            # Assumes that the 'validate_data' method will load the default
            # values into the configuration files, and assumes that an empty
            # dict is a valid configuration.
            return dict()
