# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.content.base import UrbdialItem

from zope.interface import implements

import zope


class IInitialParcel(zope.interface.Interface):
    """
    Schema for DataGridField widget's row of field 'initial_estate'
    """


class InitialParcel(UrbdialItem):
    """
    InitialParcel dexterity class
    """
    implements(IInitialParcel)

    __ac_local_roles_block__ = True
