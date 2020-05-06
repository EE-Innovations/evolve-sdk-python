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

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from zepben.cimbend.cim.iec61970.base.core.identified_object import IdentifiedObject

__all__ = ["OrganisationRole"]


@dataclass
class OrganisationRole(IdentifiedObject):
    """
    Identifies a way in which an organisation may participate in the utility enterprise (e.g., customer, manufacturer, etc).
    Attributes -
        organisation: The :class:`zepben.cimbend.iec61968.common.organisation.Organisation` having this role.
    """
    organisation: Optional[Organisation] = None
