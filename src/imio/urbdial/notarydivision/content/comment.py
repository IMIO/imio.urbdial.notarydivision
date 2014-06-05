# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision import _

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
    Comment dexterity schema
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
    Comment dexterity class
    """
    implements(IComment)

    __ac_local_roles_block__ = True
