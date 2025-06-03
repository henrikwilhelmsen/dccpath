# Copyright (C) 2025 Henrik Wilhelmsen.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at <https://mozilla.org/MPL/2.0/>.

"""Maya tests module."""

import os
from collections.abc import Callable
from pathlib import Path

import pytest

from dccpath import get_maya, get_mayapy
from dccpath._maya import MAYA_EXE_NAME, MAYAPY_EXE_NAME


@pytest.mark.parametrize(
    argnames=("maya_name", "fn"),
    argvalues=[
        (MAYA_EXE_NAME, get_maya),
        (MAYAPY_EXE_NAME, get_mayapy),
    ],
)
def test_get_maya_env_var(
    tmp_path: Path,
    maya_name: str,
    fn: Callable[[str], Path],
) -> None:
    """Test that the function returns path to Maya when MAYA_LOCATION env var is set."""
    version = os.getenv("MAYA_VERSION", default="2025")
    maya_install_dir = tmp_path / f"maya{version}"
    maya_bin = maya_install_dir / "bin"
    maya = maya_bin / maya_name
    old_env = os.environ

    maya_bin.mkdir(parents=True)
    maya.touch()
    os.environ["MAYA_LOCATION"] = maya_install_dir.as_posix()

    try:
        result = fn(version)

    finally:
        os.environ.clear()
        os.environ.update(old_env)

    assert result == maya
