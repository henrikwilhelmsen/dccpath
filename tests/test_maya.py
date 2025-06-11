# Copyright (C) 2025 Henrik Wilhelmsen.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at <https://mozilla.org/MPL/2.0/>.

"""Maya tests module."""

import functools
from collections.abc import Callable
from pathlib import Path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem, OSType

from dccpath import get_maya, get_mayapy


@pytest.mark.parametrize(
    argnames=("test_fn", "version", "os_type", "exe_name"),
    argvalues=[
        (get_maya, "2020", OSType.WINDOWS, "maya.exe"),
        (get_maya, "2022", OSType.MACOS, "maya"),
        (get_maya, "2020", OSType.LINUX, "maya"),
        (get_mayapy, "2028", OSType.LINUX, "mayapy"),
        (get_mayapy, "2019", OSType.MACOS, "mayapy"),
        (get_mayapy, "2020", OSType.WINDOWS, "mayapy.exe"),
    ],
)
def test_get_maya_env_var(  # noqa: PLR0913
    test_fn: Callable[[str], Path],
    version: str,
    exe_name: str,
    os_type: OSType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    fs: FakeFilesystem,
) -> None:
    """Test that the function returns path to exe when MAYA_LOCATION env var is set."""
    fs.os = os_type

    maya_location = tmp_path / f"maya{version}"
    maya = maya_location / "bin" / exe_name

    _ = fs.create_file(maya)  # pyright: ignore[reportUnknownMemberType]

    if os_type == OSType.WINDOWS:
        current_platform = "Windows"
    elif os_type == OSType.MACOS:
        current_platform = "Darwin"
    else:
        current_platform = "Linux"

    monkeypatch.setattr("dccpath._maya.CURRENT_PLATFORM", current_platform)
    monkeypatch.setenv("MAYA_LOCATION", maya_location.as_posix())
    result = test_fn(version)

    assert result.as_posix() == maya.as_posix()


@pytest.mark.parametrize(
    argnames=("test_fn", "os_type", "expected"),
    argvalues=[
        (
            functools.partial(get_maya, "2023"),
            OSType.WINDOWS,
            Path(
                "C:/Program Files/Autodesk/Maya2023/bin/maya.exe",
            ),
        ),
        (
            functools.partial(get_maya, "2026"),
            OSType.MACOS,
            Path("/Applications/Autodesk/maya2026/Maya.app/Contents/bin/maya"),
        ),
        (
            functools.partial(get_maya, "2026"),
            OSType.LINUX,
            Path("/usr/autodesk/maya2026/bin/maya"),
        ),
        (
            functools.partial(get_mayapy, "2023"),
            OSType.WINDOWS,
            Path(
                "C:/Program Files/Autodesk/Maya2023/bin/mayapy.exe",
            ),
        ),
        (
            functools.partial(get_mayapy, "2026"),
            OSType.MACOS,
            Path("/Applications/Autodesk/maya2026/Maya.app/Contents/bin/mayapy"),
        ),
        (
            functools.partial(get_mayapy, "2026"),
            OSType.LINUX,
            Path("/usr/autodesk/maya2026/bin/mayapy"),
        ),
    ],
)
def test_get_maya_mayapy(
    test_fn: Callable[[], Path],
    os_type: OSType,
    expected: Path,
    fs: FakeFilesystem,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that the correct path is returned for a given version and OS type."""
    if os_type == OSType.WINDOWS:
        current_platform = "Windows"
    elif os_type == OSType.MACOS:
        current_platform = "Darwin"
    else:
        current_platform = "Linux"

    monkeypatch.setattr("dccpath._maya.CURRENT_PLATFORM", current_platform)
    fs.os = os_type
    _ = fs.create_file(expected)  # pyright: ignore[reportUnknownMemberType]
    maya_path = test_fn()

    assert maya_path.as_posix() == expected.as_posix()
