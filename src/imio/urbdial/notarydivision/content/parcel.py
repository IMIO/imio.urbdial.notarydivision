# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.content.base import UrbdialItem

from zope.interface import implements

import zope


class IInitialParcel(zope.interface.Interface):
    """
    Schema of InitialParcel
    """


class InitialParcel(UrbdialItem):
    """
    InitialParcel dexterity class
    """
    implements(IInitialParcel)

    __ac_local_roles_block__ = True


class ICreatedParcel(IInitialParcel):
    """
    Schema of CreatedParcel
    """


class CreatedParcel(InitialParcel):
    """
    CreatedParcel dexterity class
    """
    implements(ICreatedParcel)
