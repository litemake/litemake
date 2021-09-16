import os
import typing


class OutputFolder:

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

    def target_id(self,
                  package: str,
                  target: str,
                  version: typing.Tuple[int, int, int],
                  ) -> str:
        return f"{package}:{target}-v{':'.join(str(v) for v in version)}"

    def archive_path(self,
                     package: str,
                     target: str,
                     version: typing.Tuple[int, int, int],
                     ) -> str:
        filename = self.target_id(package, target, version) + '.a'
        return os.path.join(self.compiled_archives_dir, filename)

    def object_path(self,
                    package: str,
                    target: str,
                    version: typing.Tuple[int, int, int],
                    relative_path: str,
                    ) -> str:
        lib = self.target_id(package, target, version)
        return os.path.join(self.compiled_objects_dir, lib, relative_path)
