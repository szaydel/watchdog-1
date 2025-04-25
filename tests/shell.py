"""
:module: tests.shell
:synopsis: Common shell operations for testing.
:author: yesudeep@google.com (Yesudeep Mangalapilly)
:author: Mickaël Schoentgen <contact@tiger-222.fr>
"""

from __future__ import annotations

import errno
import os
import os.path
import shutil
import tempfile
import time


def cd(path):
    os.chdir(path)


def pwd():
    return os.getcwd()


def mkfile(path):
    """Creates a file"""
    with open(path, "ab"):
        pass


def mkdir(path, *, parents=False):
    """Creates a directory (optionally also creates all the parent directories
    in the path)."""
    if parents:
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    else:
        os.mkdir(path)


def symlink(source, destination, *, target_is_directory: bool = False):
    os.symlink(source, destination, target_is_directory=target_is_directory)


def rm(path, *, recursive=False):
    """Deletes files or directories."""
    if os.path.isdir(path):
        if recursive:
            shutil.rmtree(path)
        else:
            raise OSError(errno.EISDIR, os.strerror(errno.EISDIR), path)
    else:
        os.remove(path)


def touch(path, times=None):
    """Updates the modified timestamp of a file or directory."""
    if os.path.isdir(path):
        os.utime(path, times)
    else:
        with open(path, "ab"):
            os.utime(path, times)


def truncate(path):
    """Truncates a file."""
    with open(path, "wb"):
        os.utime(path, None)


def mv(src_path, dest_path):
    """Moves files or directories."""
    try:
        os.rename(src_path, dest_path)
    except OSError:
        # this will happen on windows
        os.remove(dest_path)
        os.rename(src_path, dest_path)


def mkdtemp():
    return tempfile.mkdtemp()


def ls(path="."):
    return os.listdir(path)


def msize(path):
    """Modify the file size without updating the modified time."""
    with open(path, "w") as w:
        w.write("")
    os.utime(path, (0, 0))
    time.sleep(0.4)
    with open(path, "w") as w:
        w.write("0")
    os.utime(path, (0, 0))


def mount_tmpfs(path):
    os.system(f"sudo mount -t tmpfs none {path}")


def unmount(path):
    os.system(f"sudo umount {path}")
