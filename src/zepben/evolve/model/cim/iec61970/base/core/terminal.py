#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional
from weakref import ref, ReferenceType

from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.evolve.model.phases import TracedPhases

__all__ = ["AcDcTerminal", "Terminal"]


class AcDcTerminal(IdentifiedObject):
    """
    An electrical connection point (AC or DC) to a piece of conducting equipment. Terminals are connected at physical
    connection points called connectivity nodes.
    """
    pass


class Terminal(AcDcTerminal):
    """
    An AC electrical connection point to a piece of conducting equipment. Terminals are connected at physical connection points called connectivity nodes.
    """

    _conducting_equipment: Optional[ConductingEquipment] = None
    """The conducting equipment of the terminal. Conducting equipment have terminals that may be connected to other conducting equipment terminals via 
    connectivity nodes."""

    phases: PhaseCode = PhaseCode.ABC
    """Represents the normal network phasing condition. If the attribute is missing three phases (ABC) shall be assumed."""

    sequence_number: int = 0
    """The orientation of the terminal connections for a multiple terminal conducting equipment. The sequence numbering starts with 1 and additional 
    terminals should follow in increasing order. The first terminal is the "starting point" for a two terminal branch."""

    traced_phases: TracedPhases = TracedPhases()
    """the phase object representing the traced phases in both the normal and current network. If properly configured you would expect the normal state phases 
    to match those in `phases`"""

    _cn: ReferenceType = None
    """This is a weak reference to the connectivity node so if a Network object goes out of scope, holding a single conducting equipment
    reference does not cause everything connected to it in the network to stay in memory."""

    def __init__(self, conducting_equipment: ConductingEquipment = None, connectivity_node: ConnectivityNode = None):
        self.conducting_equipment = conducting_equipment
        if connectivity_node:
            self.connectivity_node = connectivity_node

    @property
    def conducting_equipment(self):
        """
        The conducting equipment of the terminal. Conducting equipment have terminals that may be connected to other conducting equipment terminals via
        connectivity nodes.
        """
        return self._conducting_equipment

    @conducting_equipment.setter
    def conducting_equipment(self, ce):
        if self._conducting_equipment is None or self._conducting_equipment is ce:
            self._conducting_equipment = ce
        else:
            raise ValueError(f"conducting_equipment for {str(self)} has already been set to {self._conducting_equipment}, cannot reset this field to {ce}")

    @property
    def connectivity_node(self):
        try:
            return self._cn()
        except TypeError:
            return None

    @connectivity_node.setter
    def connectivity_node(self, cn):
        self._cn = ref(cn)

    @property
    def connected(self) -> bool:
        if self.connectivity_node:
            return True
        return False

    @property
    def connectivity_node_id(self):
        return self.connectivity_node.mrid if self.connectivity_node is not None else None

    def __repr__(self):
        return f"Terminal{{{self.mrid}}}"

    def get_switch(self):
        """
        Get any associated switch for this Terminal
        Returns Switch if present in this terminals ConnectivityNode, else None
        """
        return self.connectivity_node.get_switch()

    @property
    def base_voltage(self):
        return self.conducting_equipment.get_base_voltage(self)

    def get_other_terminals(self):
        return [t for t in self.conducting_equipment.terminals if t is not self]

    def connect(self, connectivity_node: ConnectivityNode):
        self.connectivity_node = connectivity_node

    def disconnect(self):
        self.connectivity_node = None

