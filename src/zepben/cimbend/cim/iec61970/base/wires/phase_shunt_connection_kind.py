"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""

from enum import Enum

__all__ = ["PhaseShuntConnectionKind"]


class PhaseShuntConnectionKind(Enum):
    # Delta Connection
    D = 0

    # Wye connection
    Y = 1

    # Wye, with neutral brought out for grounding.
    Yn = 2

    # Independent winding, for single-phase connections.
    I = 3

    # Ground connection; use when explicit connection to ground needs to be expressed in combination with the phase
    # code, such as for electrical wire/cable or for meters.
    G = 4

    # Unrecognised
    UNRECOGNIZED = 5

    @property
    def short_name(self):
        return str(self)[25:]
