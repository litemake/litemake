import pytest
from tests.utils import VirtualProject, matching_msg
from litemake.parse.endpoints import FolderPathTemplate
from litemake.exceptions import litemakeTemplateError

import os.path


@pytest.mark.parametrize('path', (0, 1, True, False, None))
def test_type_mismatches(path):
    """ Tests that if not a string is provided to the template validation
    process, raises an appropriate error. """

    template = FolderPathTemplate()
    with pytest.raises(litemakeTemplateError) as err:
        template.validate(path, list())

    assert matching_msg('expected type', err.value.raw_msg)


@pytest.mark.parametrize('path', ('example/',))
def test_existing_folder_path(path: str, project: VirtualProject):
    """ Tests that the template validation of the 'FolderPathTemplate' passes
    if the given folder path exists. """
    path = project.add_dir(path)
    template = FolderPathTemplate()
    template.validate(path, list())


@pytest.mark.parametrize('path', ('example/',))
def test_non_existing_folder_path(path: str, project: VirtualProject):
    """ Tests that the template validation of the 'FolderPathTemplate' passes
    if the given folder path doesn't exist. """
    path = os.path.join(project.basepath, path)
    FolderPathTemplate().validate(path, list())


def test_file_instead_of_folder(project: VirtualProject):
    """ Tests that the folder template supports a path to an existing
    folder. """

    path = project.add_file('somefile.txt', 'Hello, world!')
    template = FolderPathTemplate()

    with pytest.raises(litemakeTemplateError) as err:
        template.validate(path, list())

    assert matching_msg('already exists', err.value.raw_msg)
