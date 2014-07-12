# -*- coding: utf-8 -*-

from collective.z3cform.rolefield.utils import add_local_roles_to_principals
from collective.z3cform.rolefield.utils import remove_local_roles_from_principals


def restrict_observation_creation_role(observation, event):
    """
    When a new observation is created, remove 'Observation Creator' role
    from the notarydivision and all its Precision.
    """
    modify_creation_role(remove_local_roles_from_principals, observation)


def restore_observation_creation_role(observation, event):
    """
    When an observation is deleted or published, restore 'Observation Creator' role
    on the notarydivision and all its Precision.
    """
    if hasattr(event, 'transition') and getattr(event.transition, 'title', '') != 'Publish':
        return

    modify_creation_role(add_local_roles_to_principals, observation)


def modify_creation_role(modifier, observation):
    notarydivision = observation.get_notarydivision()
    precisions = notarydivision.get_comments(portal_type='Precision', state='Published')
    groups = observation.get_local_group()
    role = observation.get_creation_role()

    modifier(notarydivision, groups, (role,))
    for precision in precisions:
        modifier(precision, groups, (role,))
