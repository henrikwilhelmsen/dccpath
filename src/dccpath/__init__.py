# Copyright (C) 2025 Henrik Wilhelmsen.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at <https://mozilla.org/MPL/2.0/>.

"""Utility library for locating DCC (Digital Content Creation) software paths."""

from ._blender import get_blender
from ._maya import get_maya, get_mayapy
from ._mobu import get_mobu, get_mobupy

__all__ = [
    "get_blender",
    "get_maya",
    "get_mayapy",
    "get_mobu",
    "get_mobupy",
]
