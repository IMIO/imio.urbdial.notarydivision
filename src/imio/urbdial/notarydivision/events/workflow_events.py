# -*- coding: utf-8 -*-

from collective.z3cform.rolefield.utils import add_local_roles_to_principals
from collective.z3cform.rolefield.utils import remove_local_roles_from_principals

from imio.helpers.security import call_as_super_user
from imio.urbdial.notarydivision.workflows.interfaces import IWorkflowStateRolesMapping

from plone import api

from zope.component import queryMultiAdapter


def update_local_roles(obj, event):
    """
    This handler is in charge of updating the local roles of an object
    depending on the mapping role/group found for the new state of this
    object's workflow.
    """

    # get workflow role/group mapping for which the transition was triggered
    workflow = event.workflow
    mapping = queryMultiAdapter((obj, workflow), IWorkflowStateRolesMapping)

    if not mapping:
        return

    # update objects local roles by removing each local role found on the
    # mapping for the old state
    old_state = event.old_state.title
    old_state_local_roles = mapping.get_group_roles_mapping_of(old_state)

    for group, roles in old_state_local_roles.iteritems():
        remove_local_roles_from_principals(obj, [group], roles)

    # update objects local roles by adding each local role found on the
    # mapping for the new state
    new_state = event.new_state.title
    new_state_local_roles = mapping.get_group_roles_mapping_of(new_state)

    for group, roles in new_state_local_roles.iteritems():
        add_local_roles_to_principals(obj, [group], roles)


def restrict_observation_creation(comment, event):
    """
    As long there is a draft observation on the notarydivision, remove
    'Observation Creator' role from the notarydivision and any Precision.
    """


def close_comments(notarydivision, event):
    """
    Delete all draft comments of a NotaryDivision when its passed or cancelled.
    Freeze all published comments of a NotaryDivision when its passed or cancelled.
    """
    if not event.new_state.title in ['Cancelled', 'Passed']:
        return

    delete_dratf_comments(notarydivision)
    freeze_comments(notarydivision)


def freeze_comments(notarydivision):

    def recursive_freeze_comments(container):
        for comment in container.objectValues():
            if comment.is_published():
                comment.transition('Freeze')
            recursive_freeze_comments(comment)

    # We have to execute recursive_freeze_comments with a super user because
    # notary user dont have the permission to trigger 'Freeze' transition on
    # comments.
    call_as_super_user(recursive_freeze_comments, container=notarydivision)


def delete_dratf_comments(notarydivision):

    def recursive_delete_draft_comments(container):
        for comment in container.objectValues():
            if comment.is_in_draft():
                api.content.delete(comment)
            else:
                recursive_delete_draft_comments(comment)

    # We have to execute recursive_delete_draft_comments with a super user because
    # notary user dont have the permission to delete comments.
    call_as_super_user(recursive_delete_draft_comments, container=notarydivision)
