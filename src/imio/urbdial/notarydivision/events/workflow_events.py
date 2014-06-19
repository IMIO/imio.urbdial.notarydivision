# -*- coding: utf-8 -*-

from collective.z3cform.rolefield.utils import add_local_roles_to_principals
from collective.z3cform.rolefield.utils import remove_local_roles_from_principals

from imio.urbdial.notarydivision.workflows.interfaces import IWorkflowStateRolesMapping

from zope.component import queryAdapter


def update_local_roles(obj, event):
    """
    This handler is in charge of updating the local roles of an object
    depending on the mapping role/group found for the new state of this
    object's workflow.
    """

    # get workflow for which the transition was triggered
    workflow = event.workflow
    mapping = queryAdapter(workflow, IWorkflowStateRolesMapping)

    if not mapping:
        return

    # update objects local roles by removing each local role found on the
    # mapping for the old state
    old_state = event.old_state.title
    old_state_local_roles = mapping.get_roles_of(old_state)
    for group, roles in old_state_local_roles.iteritems():
        remove_local_roles_from_principals(obj, [group], roles)

    # update objects local roles by adding each local role found on the
    # mapping for the new state
    new_state = event.new_state.title
    new_state_local_roles = mapping.get_roles_of(new_state)
    for group, roles in new_state_local_roles.iteritems():
        add_local_roles_to_principals(obj, [group], roles)