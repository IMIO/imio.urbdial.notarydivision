# -*- coding: utf-8 -*-

from plone.dexterity.browser import add
from plone.dexterity.browser import edit
from plone.dexterity.browser import view

from z3c.form import interfaces
from z3c.form import term
from z3c.form.browser.checkbox import SingleCheckBoxWidget
from z3c.form.interfaces import ICheckBoxWidget
from z3c.form.widget import FieldWidget

from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import zope


class NotaryDivisionAddForm(add.DefaultAddForm):
    """
    NotaryDivision custom Add form.
    """


class NotaryDivisionAddView(add.DefaultAddView):
    """
    NotaryDivision custom AddView.
    Required to customize AddForm:
    - first we override the attr 'form' with our custom AddForm.
    - then we register the AddView for our NotaryDivision FTI.
    """
    form = NotaryDivisionAddForm


class NotaryDivisionEditForm(edit.DefaultEditForm):
    """
    NotaryDivision custom Edit form.
    """


class NotaryDivisionView(view.DefaultView):
    """
    NotaryDivision custom View.
    """


class ISingleCheckBoxDataGridWidget(ICheckBoxWidget):
    """Single Checbox widget for datagrid."""


class SingleCheckBoxDataGridWidget(SingleCheckBoxWidget):
    """ """
    implements(ISingleCheckBoxDataGridWidget)

    def displayValue(self):
        if self.value:
            return 'True'
        return 'False'

    def updateTerms(self):
        if self.terms is None:
            self.terms = term.Terms()
            if self.context is interfaces.NO_VALUE:
                val = False
            else:
                val = self.context[self.field.getName()]
            terms = (SimpleTerm('selected', 'selected', val),)
            self.terms.terms = SimpleVocabulary(terms)
        return self.terms


@zope.interface.implementer(interfaces.IFieldWidget)
def SingleCheckBoxDataGridFieldWidget(field, request):
    """IFieldWidget factory for CheckBoxWidget."""
    widget = FieldWidget(field, SingleCheckBoxDataGridWidget(request))
    widget.label = u''  # don't show the label twice
    return widget
