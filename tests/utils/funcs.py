import os


def matching_msg(expected: str, got: str) -> bool:
    """ Checks if the 'got' string contains the 'expected' string. Returns
    True only if the 'got' string is contained inside the 'expected' string. """
    expected, got = expected.lower(), got.lower()
    return expected in got


class change_cwd:
    """ A simple function-like class that when used with the 'with' keyword,
    changes the current work directory, and when exiting the 'with' scope,
    changes it back to the previous value.

    ## Usage

    ```python
        with change_cwd('/abs/path/to/new/cwd/'):
            # do something with new working directory
            somthing_in_new_work_dir()

        # automatically returns to the previous value.
        somthing_with_old_work_dir()
    ```
    """

    def __init__(self, newcwd: str) -> None:
        self.newcwd = newcwd
        self.oldcwd = None

    def __enter__(self) -> None:
        self.oldcwd = os.getcwd()
        os.chdir(self.newcwd)

    def __exit__(self, *_) -> None:
        if self.oldcwd:
            os.chdir(self.oldcwd)
            self.oldcwd = None
