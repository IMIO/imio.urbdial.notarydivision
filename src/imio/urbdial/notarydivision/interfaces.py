# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from plone.dexterity.interfaces import IDexterityFTI

from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IImioUrbdialNotarydivisionLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class INotaryDivisionFTI(IDexterityFTI):
    """Marker interface for NotaryDivision FTI."""
