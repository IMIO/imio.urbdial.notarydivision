# -*- coding: utf-8 -*-

from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow

from five import grok

from imio.urbdial.notarydivision import _

from plone.dexterity.content import Container
from plone.directives import dexterity
from plone.supermodel import model

from z3c.form import field

from zope import schema
from zope.interface import implements

import zope


# DataGridField schemas #

class IApplicantsRowSchema(zope.interface.Interface):
    """
    Schema for DataGridField widget's row of field 'applicants'
    """
    name = schema.TextLine(
        title=_(u'Name'),
        required=False,
    )

    firstname = schema.TextLine(
        title=_(u'Firstname'),
        required=False,
    )

# DataGridField schemas end #


# NotaryDivision schema #

class INotaryDivision(model.Schema):
    """
    NotaryDivision dexterity schema
    """

    reference = schema.TextLine(
        title=_(u'Reference'),
        required=False,
    )
    applicants = schema.List(
        title=_(u'Applicants'),
        required=False,
        value_type=DictRow(
            schema=IApplicantsRowSchema,
            required=False
        ),
    )


class NotaryDivision(Container):
    """
    NotaryDivision dexterity class
    """
    implements(INotaryDivision)
    grok.name('NotaryDivision')

    __ac_local_roles_block__ = True


class NotaryDivisionAddForm(dexterity.AddForm):
    grok.name('NotaryDivision')
    grok.require('imio.urbdial.notarydivision.AddNotaryDivision')

    fields = field.Fields(INotaryDivision)
    fields['applicants'].widgetFactory = DataGridFieldFactory
