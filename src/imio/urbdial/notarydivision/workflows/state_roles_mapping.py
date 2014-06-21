# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.workflows.interfaces import IWorkflowStateRolesMapping

from zope.interface import implements


class WorkflowStateRolesMapping(object):
    """
    Store mapping between roles and groups for each state of a given workflow.
    This mapping is registered as a named adapter for an object and a workflow
    of this object.
    """
    implements(IWorkflowStateRolesMapping)

    mapping = {}

    def __init__(obj, workflow):
        pass

    def get_roles_of(self, state):
        return self.mapping.get(state, {})
