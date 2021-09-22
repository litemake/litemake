import os
from abc import ABC

import toml
from toml import TomlDecodeError

from .info import PackageInfo
from litemake.constants import DEFAULT_SETUP_FILENAME

from litemake.exceptions import (
    litemakeSetupFileNotFoundError,
    litemakeParsingError,
    litemakeTemplateError,
)


class Package(ABC):
    pass


class LocalPackage(Package):

    def __init__(self, basepath: str, configfile: str = None):
        self.basepath = basepath

        configfile = configfile or DEFAULT_SETUP_FILENAME
        configpath = os.path.join(basepath, configfile)

        try:
            with open(configpath, mode='r', encoding='utf8') as file:
                data = toml.load(file)

        except FileNotFoundError:
            raise litemakeSetupFileNotFoundError(configfile) from None

        except TomlDecodeError as err:
            raise litemakeParsingError(
                filename=configpath,
                line=err.lineno,
                col=err.colno,
                msg=err.msg,
            ) from None

        try:
            self._info = PackageInfo(data)

        except litemakeTemplateError as err:
            raise err.to_config_error(configpath)

    def __getattr__(self, name: str):
        return self._info.__getattribute__(name)
