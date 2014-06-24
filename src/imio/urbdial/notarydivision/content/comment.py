# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision import _
from imio.urbdial.notarydivision.content.interfaces import INotaryDivisionElement

from plone import api
from plone.app import textfield
from plone.autoform import directives as form
from plone.dexterity.content import Container
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


class Comment(Container):
    """
    Comment dexterity class.
    """
    implements(IComment)

    __ac_local_roles_block__ = True

    def get_notarydivision(self):
        level = self
        while(level.portal_type != 'NotaryDivision'):
            level = level.aq_parent
        return level

    def is_published(self):
        is_published = api.content.get_state(self) in ['Published', 'Frozen']
        return is_published

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

    def get_creation_date(self):
        creation_action = self.workflow_history.values()[0][0]
        return creation_action.get('time')


class IObservation(IComment):
    """
    Observation dexterity schema.
    """


class Observation(Comment):
    """
    Observation dexterity class.
    """
    implements(IObservation)


class IPrecision(IComment):
    """
    Precision dexterity schema.
    """


class Precision(Comment):
    """
    Precision dexterity class.
    """
    implements(IPrecision)


class IPrecisionDemand(IObservation):
    """
    Precision demand dexterity schema.
    """


class PrecisionDemand(Observation):
    """
    Precision demand dexterity class.
    """
    implements(IObservation)


class IInadmissibleFolder(IObservation):
    """
    Inadmissible folder dexterity schema.
    """


class InadmissibleFolder(Observation):
    """
    Inadmissible folder dexterity class.
    """
    implements(IObservation)
