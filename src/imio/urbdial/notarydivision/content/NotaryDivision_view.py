# -*- coding: utf-8 -*-

from collective.z3cform.datagridfield.datagridfield import DataGridField

from plone.dexterity.browser import add
from plone.dexterity.browser import edit
from plone.dexterity.browser import view

from z3c.form import interfaces
from z3c.form.widget import FieldWidget

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


class InitialEstateDataGridField(DataGridField):
    """Custom DataGridField for 'initial_estate' field."""

    def display_initial_state_line(self, line):
        """
        Render HTMl display of a line value of initial_estate field.
        """
        locality = self.get_display_value('locality', line)
        reference = self._get_initial_state_reference(line)
        surface = self.get_display_value('surface', line)
        specific_rights = self.get_display_value('specific_rights', line)

        display_line = u'<td>{locality}</td><td>{reference}</td><td>{surface}</td><td>{specific_rights}</td>'.format(
            locality=locality,
            reference=reference,
            surface=surface,
            specific_rights=specific_rights,
        )

        return display_line

    def _get_initial_state_reference(self, line):
        reference_fields = ['division', 'section', 'radical', 'bis', 'exposant', 'power']
        reference_values = [line[name] for name in reference_fields if line[name] is not None]
        reference = ' '.join(reference_values)
        return reference

    def get_display_value(self, value_name, line):
        val = line[value_name]
        if val is None:
            val = '<span class="discreet">N.C</span>'
        return val


@zope.interface.implementer(interfaces.IFieldWidget)
def initial_estate_DataGridFieldFactory(field, request):
    """IFieldWidget factory for InitialEstateDataGridField."""
    return FieldWidget(field, InitialEstateDataGridField(request))
