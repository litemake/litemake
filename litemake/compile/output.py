import os
import typing


class litemakeOutputFolder:

    def __init__(self, basepath: str):
        self.basepath = basepath

    def __call__(self, *args):
        return os.path.join(self.basepath, *args)

    @property
    def compiled_archives_dir(self):
        return self('archives/')

    @property
    def compiled_objects_dir(self):
        return self('objects/')

    def library_id(self,
                   name: str,
                   version: typing.Tuple[int, int, int],
                   ) -> str:
        return f"{name}-v{':'.join(str(v) for v in version)}"

    def archive_path(self,
                     name: str,
                     version: typing.Tuple[int, int, int],
                     ) -> str:
        filename = self.library_id(name, version) + '.a'
        return os.path.join(self.compiled_archives_dir, filename)

    def object_path(self,
                    lib_name: str,
                    lib_version: typing.Tuple[int, int, int],
                    relative_path: str,
                    ) -> str:
        lib = self.library_id(lib_name, lib_version)
        return os.path.join(self.compiled_objects_dir, lib, relative_path)
