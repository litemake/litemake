import os
import typing
from abc import ABC

from .parser import PackageParser
from litemake.constants import DEFAULT_SETUP_FILENAME


class Package(ABC):
    pass


class LocalPackage(Package):

    def __init__(self, basedir: str, configfile: str = None):
        configfile = configfile or DEFAULT_SETUP_FILENAME
        configpath = os.path.join(basedir, configfile)
        self._parser = PackageParser(configpath)

    @property
    def name(self,) -> str:
        """ The name of the package, as a string. """
        return self._parser.package_name

    @property
    def description(self,) -> str:
        """ A sentence or two that describe the package, as a string. """
        val = self._parser.package_description
        return val if val else None

    @property
    def author(self,) -> str:
        """ The name of the author of the package, as a string. """
        val = self._parser.package_author
        return val if val else None

    @property
    def version(self,) -> typing.Tuple[int, int, int]:
        """ A tuple that represents the current version of the package.
        The values in the tuple are positive integers that represent
        the version number following the Semantic Versioning convention
        (https://semver.org/). """
        return self._parser.package_version[:3]

    @property
    def version_label(self,) -> typing.Optional[str]:
        """ A short string that adds information about the version (for example,
        'alpha', 'experimental', etc). If this is a "regular" release version,
        the value returned should be `None`. """
        val = self._parser.package_version[3]
        return val if val else None

    @property
    def identifier(self,) -> str:
        """ A unique string that represents the current version of the
        package. """

        id = f"{self.name}-v{'.'.join(self.version)}"
        if self.version_label:
            id += f'-{self.version_label}'
        return id
