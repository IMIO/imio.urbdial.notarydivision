# -*- coding: utf-8 -*-

from plone import api

from zope.component import getUtility
from zope.i18n.interfaces import ITranslationDomain


def translate(msgid, domain='urbdial.divnot', target_language='fr'):
    translation_domain = getUtility(ITranslationDomain, domain)
    translation = translation_domain.translate(
        msgid,
        target_language=target_language,
        default=msgid
    )
    return translation


def get_pod_templates_folder():
    portal = api.portal.getSite()
    return portal.pod_templates


def get_notarydivision(obj):
    if obj.portal_type == 'NotaryDivision':
        return obj
    if hasattr(obj, 'get_notarydivision'):
        return obj.get_notarydivision()
