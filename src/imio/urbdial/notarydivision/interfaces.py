# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from plone.dexterity.interfaces import IDexterityFTI

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IImioUrbdialNotarydivisionLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ICommentFTI(IDexterityFTI):
    """Marker interface for Comment FTI's."""


class INotaryDivisionFTI(IDexterityFTI):
    """Marker interface for NotaryDivision FTI."""


class IOtherNotaryDivisionFTI(IDexterityFTI):
    """Marker interface for NotaryDivision FTI."""


class ICreatedParcellingFTI(IDexterityFTI):
    """Marker interface for CreatedParcelling FTI."""


class IAvailableDocumentsForGeneration(Interface):
    """Adapt a context and a request to provide a list of PODTemplate."""

    def get_available_templates(self):
        """
        Return a list of PODTemplate which can be generated on the
        adapted context.
        """


class IAutoIncrementInt(Interface):
    """Marker interface for AutoIncrementInt zope.schema field."""
