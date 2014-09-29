# -*- coding: utf-8 -*-

from collective.z3cform.rolefield.utils import remove_local_roles_from_principals

from imio.urbdial.notarydivision.utils import get_notary_groups

from plone import api


def remove_owner_role(obj, event):
    """
    Remove Owner role from NotaryDivision any object it contains.
    """
    user = api.user.get_current()
    remove_local_roles_from_principals(obj, [user.id], ('Owner',))


def set_notary_office_field(divnot, event):
    """
    Assign value to the hidden field 'notary_office'.
    This value is the notary_office group of the user who created the
    notarydivision.
    """
    # if the value has already been assigned (by an admin), skip
    if divnot.notary_office:
        return

    current_user = api.user.get_current()
    user_notary_groups = get_notary_groups(current_user)
    user_notary_offices = set([g.id for g in user_notary_groups])

    divnot.notary_office = user_notary_offices
