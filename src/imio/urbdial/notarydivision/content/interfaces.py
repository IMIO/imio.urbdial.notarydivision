# -*- coding: utf-8 -*-

from zope.interface import Interface


class INotaryDivisionElement(Interface):
    """Marker interface for every item in a NotaryDivision (self included)."""


class IObservation(Interface):
    """Marker interface for all FD and Township comments."""
