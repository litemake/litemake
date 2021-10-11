import os
import subprocess
import platform

import pytest


def matching_msg(expected: str, got: str) -> bool:
    """Checks if the 'got' string contains the 'expected' string. Returns
    True only if the 'got' string is contained inside the 'expected' string."""
    expected, got = expected.lower(), got.lower()
    return expected in got


class change_cwd:
    """A simple function-like class that when used with the 'with' keyword,
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


def execute(*cmd: str) -> str:
    """Executes the given command, asserts that the return code is zero and
    returns the captured stdout stream."""

    result = subprocess.run(
        *cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    assert result.returncode == 0, "Return code of compiled program isn't 0"
    return result.stdout


def skip_os(os_name: str):
    """A decorator that uses the 'pytest.mark.skipif' decorator and applies it
    to the decorated test function/class if the current os matches the given os
    string."""

    def decorator(func):
        sys = platform.system()
        dec = pytest.mark.skipif(
            sys.lower() == os_name.lower(),
            reason=f"Operation system {sys} doesn't support this test",
        )
        return dec(func)

    return decorator


skip_windows = skip_os("windows")
skip_linux = skip_os("linux")
skip_macos = skip_os("darwin")
