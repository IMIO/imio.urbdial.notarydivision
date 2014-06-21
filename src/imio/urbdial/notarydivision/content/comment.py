# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision import _
from imio.urbdial.notarydivision.utils import translate

from plone import api
from plone.app import textfield
from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.formwidget.multifile import MultiFileFieldWidget
from plone.namedfile import field
from plone.supermodel import model

from zope import schema
from zope.interface import implements


class IComment(model.Schema):
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

    @property
    def full_title(self):
        type_ = translate(_(self.portal_type))

        author = api.user.get(self.creators[0])
        author = author.getUserName()
        history = self.workflow_history.get('Observation_workflow')[-1]
        action = history.get('action') == 'Publish' and 'publié' or 'créé'
        date = history.get('time').strftime('%d/%m/%Y à %H:%M')
        warning = history.get('action') == 'Publish' and ' ' or ' (BROUILLON NON PUBLIÉ)'

        publication = '{action} le {date}{warning}'.format(
            action=action,
            date=date,
            warning=warning,
        )

        title = '{type_} par {author}, {publication}:'.format(
            type_=type_,
            author=author,
            publication=publication,
        )
        return title

    def get_notarydivision(self):
        level = self
        while(level.portal_type != 'NotaryDivision'):
            level = level.aq_parent
        return level


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
