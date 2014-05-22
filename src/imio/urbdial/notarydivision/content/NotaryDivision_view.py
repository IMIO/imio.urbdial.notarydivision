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


class EstateDataGridField(DataGridField):
    """Custom DataGridField for 'initial_estate' field."""

    def display_initial_state(self):
        """
        Render table HTML display of initial_estate datagrid.
        """
        if not self.value:
            return u''

        table_lines = []

        for line in self.value:
            display_line = self.get_line_display(line)
            table_line = u'<tr>{}</tr>'.format(display_line)
            table_lines.append(table_line)

        html_table = u''.join(table_lines)

        return html_table

    def get_line_display(self, line):
        """
        Render HTML table line display of a line value of initial_estate datagrid.
        """
        index = self.value.index(line)
        datagrid_widget = self.widgets[index]

        reference_field_ids = ['division', 'section', 'radical', 'bis', 'exposant', 'power']

        display_line = []
        for field_id, widget in datagrid_widget.subform.widgets.items():
            if field_id not in reference_field_ids:
                cell_value = self.get_display_value(field_id, line)
                html_cell = u'<td>{value}</td>'.format(value=cell_value)
                display_line.append(html_cell)

            elif field_id == 'division':
                reference = self.get_reference_display(line)
                html_cell = u'<td>{value}</td>'.format(value=reference)
                display_line.append(html_cell)

        html_line = u''.join(display_line)
        return html_line

    def get_reference_display(self, line):
        """
        Render HTML cell of cadastral reference value.
        """
        reference_fields = ['division', 'section', 'radical', 'bis', 'exposant', 'power']
        reference_values = [line[name] for name in reference_fields if line[name] is not None]
        reference = ' '.join(reference_values)
        return reference

    def get_display_value(self, field_id, line):
        val = line[field_id]
        if not val:
            display_value = '<span class="discreet">N.C</span>'
        else:
            index = self.value.index(line)
            widget = self.widgets[index].subform.widgets[field_id]
            display_value = widget.render()
        return display_value


@zope.interface.implementer(interfaces.IFieldWidget)
def estate_DataGridFieldFactory(field, request):
    """IFieldWidget factory for EstateDataGridField."""
    return FieldWidget(field, EstateDataGridField(request))
