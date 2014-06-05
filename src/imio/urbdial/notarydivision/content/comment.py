# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision import _

from plone.app import textfield

from plone.dexterity.content import Container

from plone.supermodel import model

from zope.interface import implements


class IComment(model.Schema):
    """
    Comment dexterity schema
    """

    text = textfield.RichText(
        title=_(u'Text'),
        required=False,
    )


class Comment(Container):
    """
    Comment dexterity class
    """
    implements(IComment)

    __ac_local_roles_block__ = True
