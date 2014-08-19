# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.interfaces import IAutoIncrementInt

from zope.interface import implements
from zope.schema import Int


class AutoIncrementInt(Int):
    """ """
    implements(IAutoIncrementInt)
