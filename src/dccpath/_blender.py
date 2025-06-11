# Copyright (C) 2025 Henrik Wilhelmsen.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at <https://mozilla.org/MPL/2.0/>.

"""Module for locating Blender paths."""

import logging
import os
import platform
import shutil
from logging import Logger
from pathlib import Path
from subprocess import check_output

logger: Logger = logging.getLogger(__name__)

CURRENT_PLATFORM = platform.system()


def get_blender_exe_version(blender_exe: str) -> str:
    # > blender --version returns "Blender <version>" followed by lines of detail
    version = check_output(
        args=[blender_exe, "--version"],
        encoding="utf-8",
        universal_newlines=True,
    ).splitlines()[0]
    return version.split(" ")[-1]


def get_blender(version: str) -> Path:
    """Get the path to the Blender executable if it exists.

    Searches PATH with `shutil.which` first, then checks platform specific default
    paths.

    On Windows: "%PROGRAMFILES%/Blender Foundation/Blender <version>/blender.exe"
    MacOS: "/Applications/Blender.app/..." first, then "/opt/homebrew/bin/blender"
    Linux: "/usr/bin/blender"

    Args:
        version: The version of Blender to get the executable for.

    Raises:
        FileNotFoundError: If a Blender executable could not be found.

    Returns:
        The path to the Blender executable if found.
    """
    program_files = os.getenv("PROGRAMFILES", default="C:/Program Files")
    default_paths = {
        "Darwin": [
            Path("/Applications/Blender.app/Contents/MacOS/Blender"),
            Path("/opt/homebrew/bin/blender"),
        ],
        "Windows": [
            Path(
                f"{program_files}/Blender Foundation/Blender {version}/blender.exe",
            ),
        ],
        "Linux": [
            Path("/usr/bin/blender"),
        ],
    }

    which_blender = shutil.which("blender")
    if (
        which_blender is not None
        and Path(which_blender).is_file()
        and version in get_blender_exe_version(blender_exe=which_blender)
    ):
        return Path(which_blender)

    try:
        platform_default_paths: list[Path] = default_paths[CURRENT_PLATFORM]
    except KeyError:
        logger.debug("No default paths for platform %s", CURRENT_PLATFORM)
        platform_default_paths = []

    for p in platform_default_paths:
        if p.is_file() and version in get_blender_exe_version(blender_exe=p.as_posix()):
            return p

    msg = f"Unable to locate a Blender {version} executable"
    raise FileNotFoundError(msg)
