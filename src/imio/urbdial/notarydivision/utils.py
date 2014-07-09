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


def get_notarydivision(context):
    if context.portal_type == 'NotaryDivision':
        return context
    return context.get_notarydivision()
