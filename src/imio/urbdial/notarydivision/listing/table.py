## -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.utils import translate

from z3c.table.column import Column


class UrbdialColumn(Column):
    """
    Base class for any z3c.table column of urbdial.notarydivision.
    """

    def renderHeadCell(self):
        """Header cell content."""
        return translate(self.header)
