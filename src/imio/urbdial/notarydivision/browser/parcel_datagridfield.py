# -*- coding: utf-8 -*-
from collective.z3cform.datagridfield.datagridfield import DataGridField

from z3c.form import interfaces
from z3c.form.widget import FieldWidget

import zope


class ParcelDataGridField(DataGridField):
    """
    Custom DataGridField for 'parcel' field.
    """

    reference_field_ids = ['division', 'section', 'radical', 'bis', 'exposant', 'power']

    def display_table_body(self):
        """
        Render table HTML display of the datagrid.
        """
        table_lines = []

        if self.value:
            for line in self.value:
                display_line = self.get_line_display(line)
                table_line = u'<tr>{}</tr>'.format(display_line)
                table_lines.append(table_line)

        table_body = u''.join(table_lines)
        return table_body

    def get_header_labels(self):
        """
        Return labels to display in header colummns.
        """
        header_labels = []

        for column in self.columns:
            if column['mode'] != 'hidden':
                field_id = column['name']
                if field_id not in self.reference_field_ids:
                    header_labels.append(column['label'])
                elif field_id == 'division':
                    header_labels.append(u'Cadastral reference')

        return header_labels

    def get_line_display(self, line):
        """
        Render HTML table line display of a line value of the datagrid.
        """
        index = self.value.index(line)
        datagrid_widget = self.widgets[index]
        display_line = []

        for field_id, widget in datagrid_widget.subform.widgets.items():
            # render cell content only if widget is not
            # hidden
            if widget.mode != 'hidden':
                if field_id not in self.reference_field_ids:
                    cell_value = self.get_display_value(field_id, line)
                    html_cell = u'<td class="datagridwidget-cell datagridwidget-cell-display">{value}</td>'.format(value=cell_value)
                    display_line.append(html_cell)

                elif field_id == 'division':
                    reference = self.get_reference_display(line)
                    html_cell = u'<td class="datagridwidget-cell datagridwidget-cell-display">{value}</td>'.format(value=reference)
                    display_line.append(html_cell)

        html_line = u''.join(display_line)
        return html_line

    def get_reference_display(self, line):
        """
        Render HTML cell of cadastral reference value.
        """
        reference_fields = ['division', 'section', 'radical', 'bis', 'exposant', 'power']
        reference = ''
        for name in reference_fields:
            val = line[name]
            if val:
                if name == 'bis':
                    reference = '{ref}/{val}'.format(ref=reference, val=val)
                else:
                    reference = '{ref} {val}'.format(ref=reference, val=val)
        return reference

    def get_display_value(self, field_id, line):
        val = line[field_id]
        if val is None or val == '' or val == u'':
            display_value = '<span class="discreet">N.C</span>'
        else:
            index = self.value.index(line)
            widget = self.widgets[index].subform.widgets[field_id]
            display_value = widget.render()
        return display_value


@zope.interface.implementer(interfaces.IFieldWidget)
def ParcelDataGridFieldFactory(field, request):
    """IFieldWidget factory for ParcelDataGridField."""
    return FieldWidget(field, ParcelDataGridField(request))
