# Copyright (C) 2025 Henrik Wilhelmsen.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at <https://mozilla.org/MPL/2.0/>.

"""Module for locating Autodesk Maya."""

import logging
import os
import platform
from pathlib import Path
from typing import Literal

logger = logging.getLogger(__name__)

MAYA_EXE_NAME: Literal["maya.exe", "maya"] = (
    "maya.exe" if platform.system() == "Windows" else "maya"
)

MAYAPY_EXE_NAME: Literal["mayapy.exe", "mayapy"] = (
    "mayapy.exe" if platform.system() == "Windows" else "mayapy"
)


def get_maya_install_dir(version: str) -> Path | None:
    """Get Maya install location on supported platforms (Linux and Windows)."""
    maya_location_var = os.environ.get("MAYA_LOCATION")

    if maya_location_var is not None and version in maya_location_var:
        install_dir = Path(maya_location_var)

        if install_dir.exists():
            return install_dir

    # Windows
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
        except FileNotFoundError:
            logger.debug(
                "Unable to locate install path for Maya %s in registry",
                version,
            )
            return None

        maya_install_dir = Path(QueryValue(reg_key, "MAYA_INSTALL_LOCATION"))
        if maya_install_dir.exists():
            logger.debug("Maya install dir located in registry: %s", maya_install_dir)
            return maya_install_dir

    # Linux
    if platform.system() == "Linux":
        maya_default_path = Path(f"/usr/autodesk/maya{version}")

        if maya_default_path.exists():
            return maya_default_path

    return None


def get_maya(version: str) -> Path | None:
    """Get the path to the maya executable."""
    install_dir = get_maya_install_dir(version=version)
    if install_dir is None:
        return None

    exe = install_dir / "bin" / MAYA_EXE_NAME
    if exe.exists():
        return exe

    return None


def get_mayapy(version: str) -> Path | None:
    """Get the path to the mayapy executable."""
    install_dir = get_maya_install_dir(version=version)
    if install_dir is None:
        return None

    exe = install_dir / "bin" / MAYAPY_EXE_NAME
    if exe.exists():
        return exe

    return None
