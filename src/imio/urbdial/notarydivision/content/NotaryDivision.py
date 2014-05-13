# -*- coding: utf-8 -*-

from five import grok

from imio.urbdial.notarydivision import _

from plone.dexterity.content import Container
from plone.directives import dexterity
from plone.supermodel import model

from zope import schema
from zope.interface import implements


class INotaryDivision(model.Schema):
    """
    """

    reference = schema.TextLine(
        title=_(u'Reference'),
        required=False,
    )


class NotaryDivision(Container):
    """
    """
    implements(INotaryDivision)
    grok.name('NotaryDivision')


class NotaryDivisionAddForm(dexterity.AddForm):
    grok.name('NotaryDivision')
    grok.require('imio.urbdial.notarydivision.AddNotaryDivision')
