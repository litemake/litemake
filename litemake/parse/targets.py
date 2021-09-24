import string
import typing
from dataclasses import dataclass

from .file import FileParser
from .templates import Template
from .endpoints import (
    DictTemplate,
    StringTemplate,
    BoolTemplate,
    ListTemplate,
    RelFolderPathTemplate,
)

SPECIAL_CHARS = '-_.'
NAME_CHARS = string.ascii_letters + string.digits + SPECIAL_CHARS


@dataclass
class TargetInfo:
    name: str
    library: bool
    sources: typing.List[str]
    include: typing.List[str]


class TargetsParser(FileParser):

    TEMPLATE = DictTemplate(
        keys=StringTemplate(
            min_len=3, max_len=30,
            allowed_chars=NAME_CHARS,
            no_repeating=SPECIAL_CHARS,
            no_on_edges=SPECIAL_CHARS,
        ),
        values=Template(
            library=BoolTemplate(default=False),
            sources=ListTemplate(
                default=list(),
                min_len=1,
                listof=StringTemplate(min_len=1),
            ),
            include=ListTemplate(
                default=list(),
                listof=RelFolderPathTemplate(),
            ),
        ),
        min_len=1,
    )

    @property
    def targets(self,) -> typing.List[str]:
        """ A list of all collected target names, as strings. """
        return list(self._data)

    @property
    def default_target(self,) -> str:
        """ The name (string) of the default collected target. """
        return self.targets[0]

    def target(self, name: str) -> typing.Optional['TargetInfo']:
        """ Returns a dataclass that represents a target with the
        given name (if exists). If a target with given name doesn't
        exist, returns `None`. """
        if name not in self.targets:
            return None

        return TargetInfo(name=name, **self._data[name])
