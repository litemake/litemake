import typing
import string

import toml
from toml import TomlDecodeError

from litemake.parse import (
    Template,
    StringTemplate,
    RelFolderPathTemplate,
    IntegerTemplate,
    BoolTemplate,
    ListTemplate,
    DictTemplate,
)

from litemake.exceptions import (
    litemakeParsingError,
    litemakeSetupFileNotFoundError,
    litemakeTemplateError,
)


class PackageParser:

    SPECIAL_CHARS = '-_.'
    NAME_CHARS = string.ascii_letters + string.digits + SPECIAL_CHARS

    TEMPLATE = Template(
        metadata=Template(
            name=StringTemplate(
                min_len=3, max_len=30,
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
                    default='', max_len=10,
                    allowed_chars=NAME_CHARS,
                    no_repeating=SPECIAL_CHARS,
                    no_on_edges=SPECIAL_CHARS,
                ),
            ),

            # TODO: c/c++ standard specification
        ),

        # TODO: custom error message when no targets provided
        target=DictTemplate(
            default=dict(),
            min_len=1,
            keys=StringTemplate(
                min_len=1, max_len=30,
                allowed_chars=NAME_CHARS,
                no_repeating=SPECIAL_CHARS,
                no_on_edges=SPECIAL_CHARS,
            ),
            values=Template(
                library=BoolTemplate(default=False),
                sources=ListTemplate(
                    default=list(),
                    listof=StringTemplate(min_len=1),
                ),
                include=ListTemplate(
                    default=list(),
                    listof=RelFolderPathTemplate(must_exist=True),
                ),
            ),
        ),
    )

    def __init__(self, filepath: str):
        self.__filepath = filepath

        try:
            with open(filepath, mode='r', encoding='utf8') as file:
                raw = toml.load(file)

        except FileNotFoundError:
            raise litemakeSetupFileNotFoundError(filepath) from None

        except TomlDecodeError as err:
            raise litemakeParsingError(
                filename=filepath,
                line=err.lineno,
                col=err.colno,
                msg=err.msg,
            ) from None

        try:
            self.__config = self.TEMPLATE.validate(raw, fieldpath=list())

        except litemakeTemplateError as err:
            raise err.to_config_error(filepath)

    @property
    def filepath(self,) -> str:
        """ The path to this configuration file. """
        return self.__filepath

    @property
    def package_name(self,) -> str:
        """ The name of the current package, as a string. """
        return self.__config['metadata']['name']

    @property
    def package_description(self,) -> str:
        """ A sentence or two that describe the package, as a string. """
        return self.__config['metadata']['description']

    @property
    def package_author(self,) -> str:
        """ The name of the author of the package, as a string. """
        return self.__config['metadata']['author']

    @property
    def package_version(self,) -> typing.Tuple[int, int, int, str]:
        """ A tuple that represents the current version of the package.
        The first 3 values in the tuple are positive integers that represent
        the version number following the Semantic Versioning convention
        (https://semver.org/), while the 4th item in the tuple is a short
        string that adds information about the version (for example, 'alpha',
        'experimental', etc). """

        ver_dict = self.__config['metadata']['version']
        return (ver_dict['major'], ver_dict['minor'], ver_dict['patch'], ver_dict['label'])

    @property
    def target_names(self,) -> typing.Set[str]:
        """ A set of strings. Each string is a name of a target that is specified
        in the configuration file. """
        return set(self.__config['target'])
