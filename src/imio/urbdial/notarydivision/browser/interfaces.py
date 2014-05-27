# -*- coding: utf-8 -*-

from z3c.form.interfaces import ICheckBoxWidget

from zope import schema


class ISingleCheckBoxForDataGridWidget(ICheckBoxWidget):
    """Single Checbox widget for datagrid."""


class IDataGridBool(schema.interfaces.IBool):
    """Marker interface for DataGridBool field."""
