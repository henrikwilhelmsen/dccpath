# Copyright (C) 2025 Henrik Wilhelmsen.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at <https://mozilla.org/MPL/2.0/>.

"""Module for locating Autodesk MotionBuilder paths."""

import logging
import platform
from pathlib import Path
from typing import Literal

logger = logging.getLogger(__name__)

CURRENT_PLATFORM = platform.system()


def get_mobu_names() -> dict[Literal["bin", "mobu", "mobupy"], str]:
    if CURRENT_PLATFORM == "Windows":
        mobu_bin = "bin/x64"
        mobu = "motionbuilder.exe"
        mobupy = "mobupy.exe"
    elif CURRENT_PLATFORM == "Linux":
        mobu_bin = "bin/linux_64"
        mobu = "motionbuilder"
        mobupy = "mobupy"
    else:
        msg = f"Platform {CURRENT_PLATFORM} not supported by MotionBuilder"
        raise FileNotFoundError(msg)

    return {"bin": mobu_bin, "mobu": mobu, "mobupy": mobupy}


def get_mobu_install_dir(version: str) -> Path:
    """Get the MotionBuilder install directory.

    Checks for the default install directory on both Linux and Windows. On Windows
    it will also check the registry if the default directory does not exist.

    See MotionBuilder documentation for the default directories:
    https://help.autodesk.com/view/MOBPRO/2025/ENU/?guid=GUID-F4D3B233-B6CF-405E-8272-E5CAB7FBF9D2

    Args:
        version: The version of MotionBuilder to get the install dir for.

    Raises:
        FileNotFoundError: If the MotionBuilder install directory cannot be found.

    Returns:
        The path to the install directory if found, else None.
    """
    default_dirs = {
        "Linux": Path(f"/usr/autodesk/MotionBuilder{version}"),
        "Windows": Path(f"C:/Program Files/Autodesk/MotionBuilder{version}"),
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
            logger.exception(
                "Unable to locate install path for MotionBuilder %s in registry",
                version,
            )

    msg = f"Unable to locate MotionBuilder {version} installation directory"
    raise FileNotFoundError(msg)


def get_mobu_exe(version: str, variant: Literal["mobu", "mobupy"]) -> Path:
    """Get the path to the MotionBuilder or mobupy executable if it exists.

    Args:
        version: The version of MotionBuilder to get the executable for.
        variant: MotionBuilder or mobupy

    Raises:
       FileNotFoundError: If the file is not found.

    Returns:
        Path to the executable if found.
    """
    try:
        install_dir = get_mobu_install_dir(version=version)
    except FileNotFoundError as e:
        msg = f"Failed to get MotionBuilder {version} installation directory"
        logger.exception(msg)
        raise FileNotFoundError(msg) from e

    try:
        names = get_mobu_names()
    except FileNotFoundError as e:
        msg = "Failed to get MotionBuilder platform paths"
        logger.exception(msg)
        raise FileNotFoundError(msg) from e

    mobu = install_dir / names["bin"] / names[variant]
    if mobu.is_file():
        return mobu

    msg = f"MotionBuilder not at expected path {mobu}, file does not exist"
    raise FileNotFoundError(msg)


def get_mobu(version: str) -> Path:
    """Get the path to the MotionBuilder executable if it exists.

    Args:
        version: The version of MotionBuilder to get the executable for.

    Raises:
       FileNotFoundError: If the file is not found.

    Returns:
        Path to the executable if found.
    """
    try:
        return get_mobu_exe(version=version, variant="mobu")
    except FileNotFoundError as e:
        msg = "Failed to locate MotionBuilder executable"
        logger.exception(msg)

        raise FileNotFoundError(msg) from e


def get_mobupy(version: str) -> Path:
    """Get the path to the mobupy executable if it exists.

    Args:
        version: The version of MotionBuilder to get the executable for.

    Raises:
       FileNotFoundError: If the file is not found.

    Returns:
        Path to the executable if found.
    """
    try:
        return get_mobu_exe(version=version, variant="mobupy")
    except FileNotFoundError as e:
        msg = "Failed to locate mobupy executable"
        logger.exception(msg)

        raise FileNotFoundError(msg) from e
