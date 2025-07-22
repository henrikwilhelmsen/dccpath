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

logger = logging.getLogger(__name__)

CURRENT_PLATFORM = platform.system()


def get_mobu_install_dir(version: str) -> Path:
    """Get the MotionBuilder install directory.

    Checks for the default install directory on both Linux and Windows. On Windows
    it will also check the registry if the default directory does not exist.

    Args:
        version: The version of MotionBuilder to get the install dir for.

    Raises:
        FileNotFoundError: If the MotionBuilder install directory cannot be found.

    Returns:
        The path to the install directory if found.
    """
    program_files = os.getenv("PROGRAMFILES", default="C:/Program Files")
    default_dirs = {
        "Linux": Path(f"/usr/autodesk/MotionBuilder {version}"),
        "Windows": Path(f"{program_files}/Autodesk/MotionBuilder {version}"),
    }
    default_path = default_dirs.get(CURRENT_PLATFORM)
    if default_path is not None and default_path.is_dir():
        return default_path

    if CURRENT_PLATFORM == "Windows":
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
            registry_dir = Path(QueryValue(reg_key, "InstallPath"))
            if registry_dir.exists():
                logger.debug("Mobu install dir located in registry: %s", registry_dir)
                return registry_dir

        except FileNotFoundError:
            logger.debug(
                "Unable to locate install path for MotionBuilder %s in registry",
                version,
            )

    msg = f"Unable to locate MotionBuilder {version} installation directory"
    raise FileNotFoundError(msg)


def get_mobu(version: str) -> Path:
    """Get the path to the MotionBuilder executable if it exists.

    Searches the default MotionBuilder installation directory, and on Windows it will
    also check the registry if the default path fails.

    Args:
        version: The version of MotionBuilder to get the executable for.

    Raises:
       FileNotFoundError: If the file is not found.

    Returns:
        Path to the executable if found.
    """
    try:
        mobu_install_dir = get_mobu_install_dir(version=version)
    except FileNotFoundError as e:
        msg = "Failed to locate MotionBuilder install dir"
        raise FileNotFoundError(msg) from e

    if CURRENT_PLATFORM == "Windows":
        mobu = mobu_install_dir / "bin" / "x64" / "motionbuilder.exe"
    elif CURRENT_PLATFORM == "Linux":
        mobu = mobu_install_dir / "bin" / "linux_64" / "motionbuilder"
    else:
        msg = f"MotionBuilder not found for platform {CURRENT_PLATFORM}"
        raise FileNotFoundError(msg)

    if mobu.is_file():
        return mobu

    msg = "Failed to locate MotionBuilder executable"
    raise FileNotFoundError(msg)


def get_mobupy(version: str) -> Path:
    """Get the path to the mobupy executable if it exists.

    Searches the default MotionBuilder installation directory, and on Windows it will
    also check the registry if the default path fails.

    Args:
        version: The version of MotionBuilder to get the executable for.

    Raises:
       FileNotFoundError: If the file is not found.

    Returns:
        Path to the executable if found.
    """
    try:
        mobu_install_dir = get_mobu_install_dir(version=version)
    except FileNotFoundError as e:
        msg = "Failed to locate MotionBuilder install dir"
        raise FileNotFoundError(msg) from e

    if CURRENT_PLATFORM == "Windows":
        mobupy = mobu_install_dir / "bin" / "x64" / "mobupy.exe"
    elif CURRENT_PLATFORM == "Linux":
        mobupy = mobu_install_dir / "bin" / "linux_64" / "mobupy"
    else:
        msg = f"Mobupy not found for platform {CURRENT_PLATFORM}"
        raise FileNotFoundError(msg)

    if mobupy.is_file():
        return mobupy

    msg = "Failed to locate Mobupy executable"
    raise FileNotFoundError(msg)
