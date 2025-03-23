# Copyright (C) 2025 Henrik Wilhelmsen.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at <https://mozilla.org/MPL/2.0/>.

"""Module for locating Autodesk MotionBuilder."""

import logging
import platform
from pathlib import Path

logger = logging.getLogger(__name__)


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
        if default_path.exists() and default_path.is_dir():
            return default_path

    if platform.system() == "Windows":
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

    logger.warning(
        "Platform %s is not supported, unable to get Mobu install dir",
        platform.system(),
    )
    return None


def _get_mobupy_linux(version: str) -> Path | None:
    mobu_install_dir = get_mobu_install_dir(version=version)

    if mobu_install_dir is not None:
        mobupy = mobu_install_dir / "bin" / "linux_64" / "mobupy"

        if mobupy.exists():
            return mobupy

    return None


def _get_mobupy_win(version: str) -> Path | None:
    mobu_install_dir = get_mobu_install_dir(version=version)

    if mobu_install_dir is not None:
        mobupy = mobu_install_dir / "bin" / "x64" / "mobupy.exe"

        if mobupy.exists():
            return mobupy

    return None


def _get_mobu_linux(version: str) -> Path | None:
    mobu_install_dir = get_mobu_install_dir(version=version)

    if mobu_install_dir is not None:
        mobupy = mobu_install_dir / "bin" / "linux_64" / "motionbuilder"

        if mobupy.exists():
            return mobupy

    return None


def _get_mobu_win(version: str) -> Path | None:
    mobu_install_dir = get_mobu_install_dir(version=version)

    if mobu_install_dir is not None:
        mobu = mobu_install_dir / "bin" / "x64" / "motionbuilder.exe"

        if mobu.exists():
            return mobu

    return None


# TODO: Refactor away the platform specific functions
def get_mobu(version: str) -> Path | None:
    """Get the path to the MotionBuilder executable if it exists.

    Args:
        version: The version of MotionBuilder to get the executable for.

    Returns:
        Path to the executable if found, else None.
    """
    if platform.system() == "Linux":
        return _get_mobu_linux(version=version)

    if platform.system() == "Windows":
        return _get_mobu_win(version=version)

    logger.warning(
        "Platform %s is not supported, unable to get Mobu executable",
        platform.system(),
    )
    return None


def get_mobupy(version: str) -> Path | None:
    """Get the path to the mobupy executable if it exists.

    Args:
        version: The version of MotionBuilder to get the executable for.

    Returns:
        Path to the executable if found, else None.
    """
    if platform.system() == "Linux":
        return _get_mobupy_linux(version=version)

    if platform.system() == "Windows":
        return _get_mobupy_win(version=version)

    logger.warning(
        "Platform %s is not supported, unable to get mobupy executable",
        platform.system(),
    )
    return None
