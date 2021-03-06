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

    # some local roles can be computed only after the object creation, we
    # need to handle that case specifically
    if not event.transition:
        mapping.object_created = False

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


def publish_draft_parcellings(notarydivision, event):
    """
    Publis all draft parcellings of a NotaryDivision when it is notified.
    """
    if not event.new_state.title == 'In investigation':
        return

    # We have to execute publish_parcellings with a super user because
    # notary user dont have the permission to trigger 'Publish' transition on
    # parcellings.
    call_as_super_user(publish_parcellings, notarydivision)


def publish_parcellings(notarydivision):
    """
    Publish draft parcellings of a NotaryDivision.
    """
    parcellings = notarydivision.get_parcellings(state='Draft')
    for parcelling in parcellings:
        parcelling.transition('Publish')


def close_comments(notarydivision, event):
    """
    Delete all draft comments of a NotaryDivision when its passed or cancelled.
    Freeze all published comments of a NotaryDivision when its passed or cancelled.
    """
    if not event.new_state.title in ['Cancelled', 'Passed']:
        return

    # We have to execute delete_draft_comments with a super user because
    # notary user dont have the permission to delete comments.
    call_as_super_user(delete_draft_comments, notarydivision)

    # We have to execute freeze_comments with a super user because
    # notary user dont have the permission to trigger 'Freeze' transition on
    # comments.
    call_as_super_user(freeze_comments, notarydivision)


def freeze_comments(notarydivision):
    """
    Freeze published comments of a NotaryDivision.
    """
    comments = notarydivision.get_comments(state='Published')
    for comment in comments:
        comment.transition('Freeze')


def delete_draft_comments(notarydivision):
    """
    Delete draft comments of a NotaryDivision.
    """
    comments = notarydivision.get_comments(state='Draft')
    for comment in comments:
        api.content.delete(comment)
