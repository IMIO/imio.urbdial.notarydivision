# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision import _
from imio.urbdial.notarydivision.content.base import UrbdialContainer
from imio.urbdial.notarydivision.content.interfaces import INotaryDivisionElement
from imio.urbdial.notarydivision.content.interfaces import IObservation

from plone.app import textfield
from plone.autoform import directives as form
from plone.formwidget.multifile import MultiFileFieldWidget
from plone.namedfile import field
from plone.supermodel import model

from zope import schema
from zope.interface import implements


class IComment(model.Schema, INotaryDivisionElement):
    """
    Comment dexterity schema.
    """

    text = textfield.RichText(
        title=_(u'Text'),
        required=False,
    )

    form.widget('files', MultiFileFieldWidget)
    files = schema.List(
        title=_(u'Files'),
        value_type=field.NamedBlobFile(),
        required=False,
    )


class Comment(UrbdialContainer):
    """
    Comment dexterity class.
    """
    implements(IComment)

    __ac_local_roles_block__ = True

    def get_notarydivision(self):
        level = self
        while(level.portal_type not in ['NotaryDivision', 'OtherNotaryDivision']):
            level = level.aq_parent
        return level

    def get_local_group(self):
        """To implement."""

    def get_creation_role(self):
        """To implement."""

    def is_in_draft(self):
        return self.get_state() == 'Draft'

    def get_creation_date(self):
        creation_action = self.workflow_history.values()[0][0]
        return creation_action.get('time')

    def get_publicator(self):
        history = self.workflow_history.values()[0]
        for action in history:
            if action.get('action') == 'Publish':
                return action.get('actor')

    def get_publication_date(self):
        history = self.workflow_history.values()[0]
        for action in history:
            if action.get('action') == 'Publish':
                return action.get('time')

    def is_frozen(self):
        return self.get_state() == 'Frozen'


class IPrecision(IComment):
    """
    Precision dexterity schema.
    """


class Precision(Comment):
    """
    Precision dexterity class.
    """
    implements(IPrecision)


class IFDObservation(IComment, IObservation):
    """
    FD Observation dexterity schema.
    """


class FDObservation(Comment):
    """
    FD Observation dexterity class.
    """
    implements(IFDObservation)

    def get_local_group(self):
        notarydivision = self.get_notarydivision()
        local_dgo4 = notarydivision.local_dgo4
        return local_dgo4

    def get_creation_role(self):
        return 'FD Observation Creator'


class IFDPrecisionDemand(IFDObservation):
    """
    FD Precision demand dexterity schema.
    """


class FDPrecisionDemand(FDObservation):
    """
    FD Precision demand dexterity class.
    """
    implements(IFDPrecisionDemand)


class IFDInadmissibleFolder(IFDObservation):
    """
    FD Inadmissible folder dexterity schema.
    """


class FDInadmissibleFolder(FDObservation):
    """
    FD Inadmissible folder dexterity class.
    """
    implements(IFDInadmissibleFolder)


class ITownshipObservation(IComment, IObservation):
    """
    Township Observation dexterity schema.
    """


class TownshipObservation(Comment):
    """
    Township Observation dexterity class.
    """
    implements(ITownshipObservation)

    def get_local_group(self):
        notarydivision = self.get_notarydivision()
        local_township = notarydivision.local_township
        return local_township

    def get_creation_role(self):
        return 'Township Observation Creator'


class ITownshipPrecisionDemand(ITownshipObservation):
    """
    Township Precision demand dexterity schema.
    """


class TownshipPrecisionDemand(TownshipObservation):
    """
    Township Precision demand dexterity class.
    """
    implements(ITownshipPrecisionDemand)


class ITownshipInadmissibleFolder(ITownshipObservation):
    """
    Township Inadmissible folder dexterity schema.
    """


class TownshipInadmissibleFolder(TownshipObservation):
    """
    Township Inadmissible folder dexterity class.
    """
    implements(ITownshipInadmissibleFolder)
