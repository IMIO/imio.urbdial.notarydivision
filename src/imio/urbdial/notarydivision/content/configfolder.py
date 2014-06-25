# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from plone.supermodel import model

from zope.interface import implements


class IConfigFolder(model.Schema):
    """
    ConfigFolder dexterity schema.
    """


class ConfigFolder(Container):
    """
    ConfigFolder dexterity class.
    """

    implements(IConfigFolder)
