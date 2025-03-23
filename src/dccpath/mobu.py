# Copyright (C) 2025 Henrik Wilhelmsen.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at <https://mozilla.org/MPL/2.0/>.

"""Module for locating Autodesk MotionBuilder paths."""

import logging
import os
import platform
from pathlib import Path
from typing import Literal

logger = logging.getLogger(__name__)

MOBU_BIN_DIR: Literal["bin/x64", "bin/linux_64"] = (
    "bin/x64" if platform.system() == "Windows" else "bin/linux_64"
)

MOBU_EXE_NAME: Literal["motionbuilder.exe", "motionbuilder"] = (
    "motionbuilder.exe" if platform.system() == "Windows" else "motionbuilder"
)

MOBUPY_EXE_NAME: Literal["mobupy.exe", "mobupy"] = (
    "mobupy.exe" if platform.system() == "Windows" else "mobupy"
)


# TODO: Check 'which mobu'
def get_mobu_install_dir(version: str) -> Path | None:
    """Get the MotionBuilder install directory.

    Checks for the default install directory on both Linux and Windows. On Windows
    it will also check the registry if the default directory does not exist.

    See MotionBuilder documentation for the default directories:
    https://help.autodesk.com/view/MOBPRO/2025/ENU/?guid=GUID-F4D3B233-B6CF-405E-8272-E5CAB7FBF9D2

    Args:
        version: The version of MotionBuilder to get the install dir for.

    Returns:
        The path to the install directory if found, else None.
    """
    if platform.system() == "Linux":
        default_path = Path(f"/usr/autodesk/MotionBuilder{version}")
        if default_path.is_dir():
            return default_path

    if platform.system() == "Windows":
        # Check default path
        program_files = os.getenv("PROGRAMFILES")
        default_path = Path(
            f"{program_files}/Autodesk/MotionBuilder {version}/bin/x64",
        )
        if default_path.is_dir():
            return default_path

        # Check registry
        from winreg import (
            HKEY_LOCAL_MACHINE,
            ConnectRegistry,
            OpenKey,
            QueryValue,
        )

        reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        try:
            reg_key = OpenKey(
                reg,
                f"SOFTWARE\\AUTODESK\\MOTIONBUILDER\\{version}",
            )
        except FileNotFoundError:
            logger.debug(
                "Unable to locate install path for MotionBuilder %s in registry",
                version,
            )
            return None

        registry_dir = Path(QueryValue(reg_key, "InstallPath"))
        if registry_dir.exists():
            logger.debug("Mobu install dir located in registry: %s", registry_dir)
            return registry_dir

    return None


def get_mobu(version: str) -> Path | None:
    """Get the path to the MotionBuilder executable if it exists.

    Args:
        version: The version of MotionBuilder to get the executable for.

    Returns:
        Path to the executable if found, else None.
    """
    install_dir = get_mobu_install_dir(version=version)
    if install_dir is None:
        return None

    mobu = install_dir / MOBU_BIN_DIR / MOBU_EXE_NAME
    if mobu.is_file():
        return mobu

    return None


def get_mobupy(version: str) -> Path | None:
    """Get the path to the mobupy executable.

    See `dccpath.mobu.get_mobu_install_dir` for details on which paths are searched.

    Args:
        version: The version of MotionBuilder to get the mobupy executable for.

    Returns:
        Path to the mobupy executable if found, else None.
    """
    install_dir = get_mobu_install_dir(version=version)
    if install_dir is None:
        return None

    mobupy = install_dir / MOBU_BIN_DIR / MOBUPY_EXE_NAME
    if mobupy.is_file():
        return mobupy

    return None
