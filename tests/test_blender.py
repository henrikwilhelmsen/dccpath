# Copyright (C) 2025 Henrik Wilhelmsen.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at <https://mozilla.org/MPL/2.0/>.

"""Blender tests module."""

from pathlib import Path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from dccpath._blender import get_blender


def test_which_blender(fs: FakeFilesystem, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that function returns the path found by shutil.which if version matches."""
    version = "4.2"
    mock_blender: str = "/usr/bin/blender"

    def mock_get_blender_exe_version(blender_exe: str) -> str:  # pyright: ignore[reportUnusedParameter]
        return version

    def mock_shutil_which(cmd: str) -> str:  # pyright: ignore[reportUnusedParameter]
        return mock_blender

    _ = fs.create_file(file_path=mock_blender)  # pyright: ignore[reportUnknownMemberType]

    monkeypatch.setattr("dccpath._blender.CURRENT_PLATFORM", "None")
    monkeypatch.setattr(
        "dccpath._blender.get_blender_exe_version",
        mock_get_blender_exe_version,
    )
    monkeypatch.setattr(
        "shutil.which",
        mock_shutil_which,
    )

    result = get_blender(version=version)
    assert result.as_posix() == mock_blender


@pytest.mark.parametrize(
    ("platform", "version", "expected_path"),
    [
        ("Linux", "4.2", Path("some_expected_path")),
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


def test_blender_raises_file_not_found_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Check that function raises FileNotFoundError when Blender is not found."""

    def mock_shutil_which(cmd: str) -> str:  # pyright: ignore[reportUnusedParameter]
        return "Foo"

    monkeypatch.setattr("dccpath._blender.CURRENT_PLATFORM", "None")
    monkeypatch.setattr(
        "shutil.which",
        mock_shutil_which,
    )
    with pytest.raises(FileNotFoundError):
        _ = get_blender(version="4.2")
