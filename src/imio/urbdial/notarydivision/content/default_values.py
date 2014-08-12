# -*- coding: utf-8 -*-

from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


@provider(IContextAwareDefaultFactory)
def initialparcel_default_number(context):
    """ """
    return 666


@provider(IContextAwareDefaultFactory)
def createdparcel_default_number(context):
    """ """
    return 999
