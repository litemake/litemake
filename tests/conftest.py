import pytest
from tests.utils import VirtualProject


@pytest.fixture
def project(request, tmpdir_factory):
    name = request.node.nodeid.replace('/', ':')
    return VirtualProject(
        name=name,
        basepath=str(tmpdir_factory.mktemp(name)),
    )
