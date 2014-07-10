# -*- coding: utf-8 -*-

from collective.z3cform.rolefield.utils import add_local_roles_to_principals
from collective.z3cform.rolefield.utils import remove_local_roles_from_principals


def restrict_observation_creation_role(observation, event):
    """
    When a new observation is created, remove 'Observation Creator' role
    from the notarydivision and all its Precision.
    """
    groups = get_groups_to_modify(observation)
    if groups:
        notarydivision = observation.get_notarydivision()
        # Remove 'Observation Creator' role from the notarydivision.
        remove_local_roles_from_principals(notarydivision, groups, ('Observation Creator',))

        precisions = notarydivision.get_comments(portal_type='Precision', state='Published')
        # Remove 'Observation Creator' role from all the Precisions.
        for precision in precisions:
            remove_local_roles_from_principals(precision, groups, ('Observation Creator',))


def restore_observation_creation_role(observation, event):
    """
    When an observation is deleted or published, restore 'Observation Creator' role
    on the notarydivision and all its Precision.
    """
    if hasattr(event, 'transition') and getattr(event.transition, 'title', '') != 'Publish':
        return

    groups = get_groups_to_modify(observation)
    if groups:
        notarydivision = observation.get_notarydivision()
        # Restore 'Observation Creator' role on the notarydivision.
        add_local_roles_to_principals(notarydivision, groups, ('Observation Creator',))

        precisions = notarydivision.get_comments(portal_type='Precision', state='Published')
        # Restore 'Observation Creator' role on all the Precisions.
        for precision in precisions:
            add_local_roles_to_principals(precision, groups, ('Observation Creator',))


def get_groups_to_modify(comment):
    """
    Get the local group of the creator of the comment.
    """
    notarydivision = comment.get_notarydivision()
    group = None
    if comment.is_dgo4_or_township() == 'dgo4':
        group = notarydivision.local_dgo4
    if comment.is_dgo4_or_township() == 'townships':
        group = notarydivision.local_township
    return group
