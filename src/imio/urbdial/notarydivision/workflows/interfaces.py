# -*- coding: utf-8 -*-

from zope.interface import Interface


class IStateLocalRolesMapping(Interface):
    """Marker interface for StateLocalRoles."""

    def get_roles_of_state(state):
        """Returns local roles of a given state."""
