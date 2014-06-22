# -*- coding: utf-8 -*-

from collective.z3cform.rolefield.utils import remove_local_roles_from_principals

from plone import api


def remove_owner_role(obj, event):
    """
    Remove Owner role from NotaryDivision any object it contains.
    """
    user = api.user.get_current()
    remove_local_roles_from_principals(obj, [user.id], ('Owner',))
