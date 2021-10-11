import os

import pytest
from tests.utils import VirtualProject, change_cwd, matching_msg

from litemake.parse.endpoints import RelFolderPathTemplate
from litemake.exceptions import litemakeTemplateError


@pytest.mark.parametrize("path", ("example/",))
def test_existing_rel_older_path(path: str, project: VirtualProject):
    project.add_dir(path)
    template = RelFolderPathTemplate()
    with change_cwd(project.basepath):
        template.validate(path, list())


@pytest.mark.parametrize("path", ("example/",))
def test_non_existing_rel_folder_path(path: str, project: VirtualProject):
    assert not os.path.isabs(path), "relative path required"
    with change_cwd(project.basepath):
        RelFolderPathTemplate().validate(path, list())


@pytest.mark.parametrize(
    "path",
    (
        "example/",
        "notafolder/",
        "one/two/three/",
        "one/two/four/",
    ),
)
def test_abs_folder_instead_of_rel(path: str, project: VirtualProject):
    project.add_dir("example/")
    project.add_dir("one/two/three/")

    abspath = os.path.join(project.basepath, path)
    template = RelFolderPathTemplate()

    with pytest.raises(litemakeTemplateError) as err:
        template.validate(abspath, list())

    assert matching_msg("Path must be relative, not absolute", err.value.raw_msg)
