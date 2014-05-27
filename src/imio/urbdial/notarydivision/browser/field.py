# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.browser.interfaces import IDataGridBool

from zope import schema
from zope.interface import implements


class DataGridBool(schema.Bool):
    """ """
    implements(IDataGridBool)
