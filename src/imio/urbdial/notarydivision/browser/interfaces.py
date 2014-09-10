# -*- coding: utf-8 -*-
from zope.interface import Interface


class IParcelTable(Interface):
    """
    Marker interface for parcel table listing.
    """


class IEditableParcelTable(Interface):
    """
    Marker interface for parcel table listing with actions column.
    """
