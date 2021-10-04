import typing
if typing.TYPE_CHECKING:
    from tests.utils import VirtualProject


from tests.utils import execute

from tests.compilers.base import skip_if_missing_clis
from litemake.compile.compilers import GplusplusCompiler


@skip_if_missing_clis(GplusplusCompiler)
def test_basic_hello_world(project: 'VirtualProject'):

    # TODO: project generation should use other avaliable compilers if g++
    # isn't avaliable. Should raise an error only if not detected compilers
    # at all.

    main_c = project.add_file('main.c', '''
    #include <stdio.h>
    int main() {
        printf("Hello from litemake!\\n");
        return 0;
    }
    ''')

    project.add_targets_file(f'''
        [build]
        sources=['{main_c}']
    ''')

    project.add_settings_file('')

    project.run('build')
    assert execute(project.join('build')) == b'Hello from litemake!\n'
