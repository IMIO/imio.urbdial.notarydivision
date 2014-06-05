# -*- coding: utf-8 -*-

from plone.dexterity.content import Container

from plone.supermodel import model

from zope.interface import implements


class IComment(model.Schema):
    """
    Comment dexterity schema
    """


class Comment(Container):
    """
    Comment dexterity class
    """
    implements(IComment)

    __ac_local_roles_block__ = True
