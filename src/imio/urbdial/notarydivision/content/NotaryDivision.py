# -*- coding: utf-8 -*-

from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow

from five import grok

from imio.urbdial.notarydivision import _

from plone.autoform import directives as form
from plone.dexterity.browser import edit
from plone.dexterity.browser import view
from plone.dexterity.content import Container
from plone.directives import dexterity
from plone.supermodel import model

from z3c.form import field
from z3c.form import interfaces

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

    form.omitted('exclude_from_nav')
    exclude_from_nav = schema.Bool(
        title=_(u'Exclude from navigation'),
        default=True,
    )

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

    __ac_local_roles_block__ = True


def setINotaryDivisionWidgetFactories():
    """
    Factorize widget factory assignment for both Edit and Add form.
    """
    fields = field.Fields(INotaryDivision)
    fields['applicants'].widgetFactory = DataGridFieldFactory
    return fields


def allFormsUpdateWidgets(widgets):
    """
    Factorize all the widget treatments that should be done for all the
    NotaryDivision forms.
    """
    widgets['exclude_from_nav'].mode = interfaces.HIDDEN_MODE


class NotaryDivisionAddForm(dexterity.AddForm):
    """
    NotaryDivision custom Add form.
    """
    grok.name('NotaryDivision')
    grok.require('imio.urbdial.notarydivision.AddNotaryDivision')

    fields = setINotaryDivisionWidgetFactories()

    def updateWidgets(self):
        super(NotaryDivisionAddForm, self).updateWidgets()
        allFormsUpdateWidgets(self.widgets)


class NotaryDivisionEditForm(edit.DefaultEditForm):
    """
    NotaryDivision custom Edit form.
    """

    fields = setINotaryDivisionWidgetFactories()

    def updateWidgets(self):
        super(NotaryDivisionEditForm, self).updateWidgets()
        allFormsUpdateWidgets(self.widgets)


class NotaryDivisionView(view.DefaultView):
    """
    NotaryDivision custom View.
    """
