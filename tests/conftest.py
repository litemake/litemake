import pytest
from tests.utils import VirtualProject

from slugify import slugify


@pytest.fixture
def project(request, tmpdir_factory):
    name = slugify(request.node.nodeid)
    return VirtualProject(
        name=name,
        basepath=str(tmpdir_factory.mktemp(name)),
    )
