# -*- coding: utf-8 -*-

from plone import api

from zope.component import getUtility
from zope.i18n.interfaces import ITranslationDomain


def translate(msgid, domain='urbdial.divnot'):
    translation_domain = getUtility(ITranslationDomain, domain)
    return translation_domain.translate(msgid, target_language='fr', default=msgid)


def get_pod_templates_folder():
    portal = api.portal.getSite()
    return portal.pod_templates


def get_notarydivision(obj):
    if obj.portal_type == 'NotaryDivision':
        return obj
    if hasattr(obj, 'get_notarydivision'):
        return obj.get_notarydivision()
