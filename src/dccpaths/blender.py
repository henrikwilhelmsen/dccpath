# Copyright (C) 2025 Henrik Wilhelmsen.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You

"""Module for locating and managing Blender."""

import logging
import os
import platform
from logging import Logger
from pathlib import Path
from typing import Literal

logger: Logger = logging.getLogger(__name__)

# Path to the Blender executable relative to the downloaded Blender dir
BLENDER_EXE_NAME: Literal["blender.exe", "blender"] = (
    "blender.exe" if platform.system() == "Windows" else "blender"
)

def get_blender(version: str) -> Path | None:
    """Get the path to the Blender executable if it exists.

    Args:
        version (BLENDER_VERSIONS): The version of Blender to get the executable for.

    Raises:
        KeyError: If a KeyError occurred when searching for existing devin-dcc Blender.

    Returns:
        Path | None: The path to the Blender executable if found, otherwise None.
    """
    # TODO: Add Linux paths from Blender Launcher

    if platform.system() == "Windows":
        program_files = os.getenv("PROGRAMFILES")

        if program_files is not None:
            default_blender = Path(
                rf"{program_files}\Blender Foundation\Blender {version}\{BLENDER_EXE_NAME}",  # noqa: E501
            )

            if default_blender.is_file():
                return default_blender

    return None
