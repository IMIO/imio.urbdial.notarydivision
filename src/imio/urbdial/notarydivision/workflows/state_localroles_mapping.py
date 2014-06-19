# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.workflows.interfaces import IStateLocalRolesMapping

from zope.interface import implements


class StateLocalRolesMapping(object):
    """
    Store mapping between roles and groups for each state of a given workflow.
    This mapping is registered as a named adapter for an object and a workflow
    of this object.
    """
    implements(IStateLocalRolesMapping)

    mapping = {}

    def get_roles_of_state(self, state):
        return self.mapping.get(state, ())
