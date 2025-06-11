# Copyright (C) 2025 Henrik Wilhelmsen.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at <https://mozilla.org/MPL/2.0/>.

"""Blender tests module."""

from pathlib import Path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem, OSType

from dccpath._blender import get_blender


def test_which_blender(fs: FakeFilesystem, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that function returns the path found by shutil.which if version matches."""
    version = "4.2"
    mock_blender: str = "/usr/bin/blender"

    _ = fs.create_file(file_path=mock_blender)  # pyright: ignore[reportUnknownMemberType]

    monkeypatch.setattr("dccpath._blender.CURRENT_PLATFORM", "None")
    monkeypatch.setattr(
        "dccpath._blender.get_blender_exe_version",
        lambda blender_exe: version,  # pyright: ignore[reportUnknownArgumentType,reportUnknownLambdaType]  # noqa: ARG005
    )
    monkeypatch.setattr(
        "shutil.which",
        lambda *args, **kwargs: mock_blender,  # pyright: ignore[reportUnknownArgumentType,reportUnknownLambdaType]  # noqa: ARG005
    )

    result = get_blender(version=version)
    assert result.as_posix() == mock_blender


@pytest.mark.parametrize(
    ("platform", "version", "expected_path"),
    [
        ("Darwin", "4.2", Path("/Applications/Blender.app/Contents/MacOS/Blender")),
        ("Darwin", "3.6", Path("/opt/homebrew/bin/blender")),
        (
            "Windows",
            "4.6",
            Path(
                "C:/Program Files/Blender Foundation/Blender 4.6/blender.exe",
            ),
        ),
        ("Linux", "5.6", Path("/usr/bin/blender")),
    ],
)
def test_get_blender(
    platform: str,
    version: str,
    expected_path: Path,
    fs: FakeFilesystem,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Check that function returns the expected path on given platform."""
    if platform == "Windows":
        fs.os = OSType.WINDOWS
    elif platform == "Darwin":
        fs.os = OSType.MACOS
    else:
        fs.os = OSType.LINUX

    monkeypatch.setattr("dccpath._blender.CURRENT_PLATFORM", platform)
    monkeypatch.setattr("shutil.which", lambda *args, **kwargs: None)  # pyright: ignore[reportUnknownArgumentType,reportUnknownLambdaType]  # noqa: ARG005
    monkeypatch.setattr(
        "dccpath._blender.get_blender_exe_version",
        lambda blender_exe: version,  # pyright: ignore[reportUnknownArgumentType,reportUnknownLambdaType]  # noqa: ARG005
    )
    _ = fs.create_file(expected_path)  # pyright: ignore[reportUnknownMemberType]
    result = get_blender(version=version)
    assert result.as_posix() == expected_path.as_posix()


def test_blender_raises_file_not_found_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Check that function raises FileNotFoundError when Blender is not found."""
    monkeypatch.setattr("dccpath._blender.CURRENT_PLATFORM", "None")
    monkeypatch.setattr(
        "shutil.which",
        lambda *args, **kwargs: None,  # pyright: ignore[reportUnknownArgumentType,reportUnknownLambdaType]  # noqa: ARG005
    )
    with pytest.raises(FileNotFoundError):
        _ = get_blender(version="4.2")
