# -*- coding: utf-8 -*-
from zope.interface import Interface


class IParcellingTable(Interface):
    """
    Marker interface for parcelling table listing.
    """


class ICreatedParcellingTable(Interface):
    """
    Marker interface for parcelling table listing.
    """


class IEditableParcellingTable(Interface):
    """
    Marker interface for parcelling table listing with actions column.
    """
