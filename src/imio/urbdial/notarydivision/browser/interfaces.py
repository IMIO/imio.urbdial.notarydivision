# -*- coding: utf-8 -*-

from z3c.form.interfaces import ICheckBoxWidget

from zope import schema
from zope.interface import Interface


class ISingleCheckBoxForDataGridWidget(ICheckBoxWidget):
    """Single Checbox widget for datagrid."""


class IDataGridBool(schema.interfaces.IBool):
    """Marker interface for DataGridBool field."""


class IAvailableDocumentsForGeneration(Interface):
    """Adapt a context and a request to provide a list of PODTemplate."""

    def get_available_templates(self):
        """
        Return a list of PODTemplate UIDs which can be generated on the
        adapted context.
        """
