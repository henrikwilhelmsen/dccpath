# Copyright (C) 2025 Henrik Wilhelmsen.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at <https://mozilla.org/MPL/2.0/>.

"""Module for locating Autodesk Maya paths."""

import logging
import os
import platform
from pathlib import Path
from typing import Literal

logger = logging.getLogger(__name__)

CURRENT_PLATFORM = platform.system()


def get_maya_exe_name(variant: Literal["maya", "mayapy"]) -> str:
    return f"{variant}.exe" if CURRENT_PLATFORM == "Windows" else variant


def get_maya_install_dir(version: str) -> Path:
    """Get the Maya install directory.

    Checks the MAYA_LOCATION variable first, then searches platform specific locations.

    On Windows: checks the registry for Maya's install location.
    On Linux: checks the default install path ('/usr/autodesk/maya<version>')

    Args:
        version: The version of Maya to get the install dir for.

    Raises:
        FileNotFoundError: If the install directory was not found.

    Returns:
        The path to the install directory if found, otherwise None.
    """
    maya_location_env = os.environ.get("MAYA_LOCATION")
    if maya_location_env is not None and version in maya_location_env:
        maya_location = Path(maya_location_env)

        if maya_location.exists():
            return maya_location

    program_files = os.getenv("PROGRAMFILES", default="C:/Program Files")
    default_paths = {
        "Darwin": Path(f"/Applications/Autodesk/maya{version}/Maya.app/Contents"),
        "Linux": Path(f"/usr/autodesk/maya{version}"),
        "Windows": Path(f"{program_files}/Autodesk/Maya{version}"),
    }

    default_path = default_paths.get(CURRENT_PLATFORM)
    if default_path is not None and default_path.is_dir():
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
                f"SOFTWARE\\AUTODESK\\MAYA\\{version}\\Setup\\InstallPath",
            )
            maya_install_dir = Path(QueryValue(reg_key, "MAYA_INSTALL_LOCATION"))

            if maya_install_dir.exists():
                return maya_install_dir

        except FileNotFoundError:
            logger.debug(
                "Unable to locate install path for Maya %s in registry",
                version,
            )

    msg = f"Unable to locate install dir for Maya {version}"
    raise FileNotFoundError(msg)


def get_maya(version: str) -> Path:
    """Get the path to the Maya executable.

    Args:
        version: The version of Maya to get the executable dir for.

    Raises:
        FileNotFoundError: If the executable was not found.

    Returns:
        The path to the Maya executable if found.

    """
    try:
        install_dir = get_maya_install_dir(version=version)
    except FileNotFoundError as e:
        msg = "Failed to locate maya install dir"
        raise FileNotFoundError(msg) from e

    exe = install_dir / "bin" / get_maya_exe_name(variant="maya")
    if exe.exists():
        return exe

    msg = f"Maya executable expected path {exe} does not exist"
    raise FileNotFoundError(msg)


def get_mayapy(version: str) -> Path:
    """Get the path to the mayapy executable.

    Args:
        version: The version of Maya to get the mayapy executable dir for.

    Raises:
        FileNotFoundError: If the executable was not found.

    Returns:
        The path to the mayapy executable if found.

    """
    try:
        install_dir = get_maya_install_dir(version=version)
    except FileNotFoundError as e:
        msg = "Failed to locate maya install dir"
        raise FileNotFoundError(msg) from e

    exe = install_dir / "bin" / get_maya_exe_name(variant="mayapy")
    if exe.exists():
        return exe

    msg = f"Mayapy executable expected path {exe} does not exist"
    raise FileNotFoundError(msg)
