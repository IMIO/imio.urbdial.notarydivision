## -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.content.notarydivision import INotaryDivision
from imio.urbdial.notarydivision.listing.interfaces import INotaryDivisionTable
from imio.urbdial.notarydivision.listing.table import UrbdialColumn

from plone import api

from z3c.table.table import Table
from z3c.table.value import ValuesMixin

from zope.interface import implements


class NotaryDivisionTable(Table):
    """
    """
    implements(INotaryDivisionTable)


class NotaryDivisionValues(ValuesMixin):
    """
    """
    @property
    def values(self):
        catalog = api.portal.get_tool('portal_catalog')
        divnot_brains = catalog(
            object_provides=INotaryDivision.__identifier__,
        )
        return divnot_brains


class TitleColumn(UrbdialColumn):
    """
    Display the title of a notarydivision.
    """

    header = 'label_colname_title'
    weight = 10

    def renderCell(self, notarydivision):
        return notarydivision.Title()
