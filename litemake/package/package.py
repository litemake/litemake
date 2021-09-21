import os
import typing
from abc import ABC, abstractmethod

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
        return self._parser.package_description

    @property
    def author(self,) -> str:
        """ The name of the author of the package, as a string. """
        return self._parser.package_author

    @property
    def version(self,) -> typing.Tuple[int, int, int, str]:
        """ A tuple that represents the current version of the package.
        The first 3 values in the tuple are positive integers that represent
        the version number following the Semantic Versioning convention
        (https://semver.org/), while the 4th item in the tuple is a short
        string that adds information about the version (for example, 'alpha',
        'experimental', etc). """

        return self._parser.package_version
