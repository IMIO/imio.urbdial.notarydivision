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


class IInitialParcelTable(IParcelTable):
    """
    Marker interface for InitialParcel table listing.
    """


class ICreatedParcelTable(IParcelTable):
    """
    Marker interface for CreatedParcel table listing.
    """
