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
from zope.security import checkPermission


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

    @property
    def full_title(self):
        type_ = translate(_(self.portal_type))

        # to update once workflow is defined for Comment
        author = api.user.get(self.creators[0])
        author = author.getUserName()
        date = '(BROUILLON NON PUBLIÉ)'

        title = '{type_} par {author}, publié le {date}:'.format(
            type_=type_,
            author=author,
            date=date
        )
        return title

    def getNotaryDivision(self):
        level = self
        while(level.portal_type != 'NotaryDivision'):
            level = level.aq_parent
        return level

    @property
    def base_permission(self):
        """To implements in subclasses with real FTI."""

    def check_permission(self, permission):
        full_permission = self.base_permission.format(
            permission=permission
        )
        return checkPermission(full_permission, self)

    def check_View_permission(self):
        return self.check_permission('View')


class IObservation(IComment):
    """
    Observation dexterity schema.
    """


class Observation(Comment):
    """
    Observation dexterity class.
    """
    implements(IObservation)

    @property
    def base_permission(self):
        return 'imio.urbdial.notarydivision.{permission}Observation'


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
