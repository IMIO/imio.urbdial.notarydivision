# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.browser.interfaces import ISingleCheckBoxForDataGridWidget

from z3c.form import interfaces
from z3c.form import term
from z3c.form.browser.checkbox import SingleCheckBoxWidget
from z3c.form.widget import FieldWidget

from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import zope


class SingleCheckBoxForDataGridWidget(SingleCheckBoxWidget):
    """
    SingleCheckBox widget which only display the form checkbox
    in a datagridfield column.
    """
    implements(ISingleCheckBoxForDataGridWidget)

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
def SingleCheckBoxForDataGridWidgetFactory(field, request):
    """IFieldWidget factory for CheckBoxWidget."""

    widget = FieldWidget(field, SingleCheckBoxForDataGridWidget(request))
    widget.label = u''  # don't show the label twice
    return widget
