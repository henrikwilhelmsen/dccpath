# Copyright (C) 2025 Henrik Wilhelmsen.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at <https://mozilla.org/MPL/2.0/>.

"""dccpath MotionBuilder tests."""

import functools
from collections.abc import Callable
from pathlib import Path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem, OSType

from dccpath import get_mobu
from dccpath._mobu import get_mobupy


@pytest.mark.parametrize(
    argnames=("test_fn", "os_type", "expected"),
    argvalues=[
        (
            functools.partial(get_mobu, "2023"),
            OSType.WINDOWS,
            Path(
                "C:/Program Files/Autodesk/MotionBuilder 2023/bin/x64/motionbuilder.exe",  # noqa: E501
            ),
        ),
        (
            functools.partial(get_mobu, "2026"),
            OSType.LINUX,
            Path("/usr/autodesk/MotionBuilder 2026/bin/linux_64/motionbuilder"),
        ),
        (
            functools.partial(get_mobupy, "2020"),
            OSType.LINUX,
            Path("/usr/autodesk/MotionBuilder 2020/bin/linux_64/mobupy"),
        ),
        (
            functools.partial(get_mobupy, "2022"),
            OSType.WINDOWS,
            Path(
                "C:/Program Files/Autodesk/MotionBuilder 2022/bin/x64/mobupy.exe",
            ),
        ),
    ],
)
def test_get_mobu_mobupy(
    test_fn: Callable[[], Path],
    os_type: OSType,
    expected: Path,
    fs: FakeFilesystem,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that the correct path is returned for a given version and OS type."""
    monkeypatch.setattr(
        "dccpath._mobu.CURRENT_PLATFORM",
        "Windows" if os_type == OSType.WINDOWS else "Linux",
    )
    fs.os = os_type
    _ = fs.create_file(expected)  # pyright: ignore[reportUnknownMemberType]
    mobu_path = test_fn()

    assert mobu_path.as_posix() == expected.as_posix()
