# -*- coding: utf-8 -*-
from zope.interface import Interface


class IParcellingTable(Interface):
    """
    Marker interface for parcelling table listing.
    """


class ICreatedParcellingTable(IParcellingTable):
    """
    Marker interface for created parcelling table listing.
    """


class IEditableParcellingTable(IParcellingTable):
    """
    Marker interface for created parcelling table listing with actions column.
    """


class INotaryDivisionTable(Interface):
    """
    Marker interface for notarydivision table listing.
    """
