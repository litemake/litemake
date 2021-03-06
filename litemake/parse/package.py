import string
import typing

from .file import FileParser
from .templates import Template
from .endpoints import StringTemplate, IntegerTemplate


SPECIAL_CHARS = "-_."
NAME_CHARS = string.ascii_letters + string.digits + SPECIAL_CHARS


class PackageParser(FileParser):
    """A parser that is responsible for parsing 'package.litemake.toml' files."""

    TEMPLATE = Template(
        name=StringTemplate(
            min_len=3,
            max_len=30,
            allowed_chars=NAME_CHARS,
            no_repeating=SPECIAL_CHARS,
            no_on_edges=SPECIAL_CHARS,
        ),
        description=StringTemplate(max_len=200, default=str()),
        author=StringTemplate(max_len=200, default=str()),
        # TODO: add metadata fields: email, url(s)
        version=Template(
            major=IntegerTemplate(range_min=0, default=0),
            minor=IntegerTemplate(range_min=0, default=0),
            patch=IntegerTemplate(range_min=0, default=0),
            label=StringTemplate(
                default="",
                max_len=10,
                allowed_chars=NAME_CHARS,
                no_repeating=SPECIAL_CHARS,
                no_on_edges=SPECIAL_CHARS,
            ),
        ),
        # TODO: c/c++ standard specification
    )

    @property
    def name(
        self,
    ) -> str:
        """The name of the current package, as a string."""
        return self._data["name"]

    @property
    def description(
        self,
    ) -> typing.Optional[str]:
        """A sentence or two that describe the package, as a string."""
        val = self._data["description"]
        return val if val else None

    @property
    def author(
        self,
    ) -> typing.Optional[str]:
        """The name of the author of the package, as a string."""
        val = self._data["author"]
        return val if val else None

    @property
    def version(
        self,
    ) -> typing.Tuple[int, int, int, str]:
        """A tuple that represents the current version of the package.
        Consists of three positive integers that represent the version number
        following the Semantic Versioning convention (https://semver.org/)."""
        ver_dict = self._data["version"]
        return (ver_dict["major"], ver_dict["minor"], ver_dict["patch"])

    @property
    def version_label(
        self,
    ) -> typing.Optional[str]:
        """A short string that adds information about the version (for example,
        'alpha', 'experimental', etc)."""
        val = self._data["version"]["label"]
        return val if val else None

    @property
    def identifier(
        self,
    ) -> str:
        """A unique string that represents the current version of the
        package."""
        id = f"{self.name}-v{'.'.join(str(v) for v in self.version)}"
        if self.version_label:
            id += f"-{self.version_label}"
        return id
