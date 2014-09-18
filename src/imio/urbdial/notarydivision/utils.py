# -*- coding: utf-8 -*-

from plone import api

from zope.component import getUtility
from zope.component import queryUtility
from zope.i18n.interfaces import ITranslationDomain
from zope.schema.interfaces import IVocabularyFactory


def translate(msgid, domain='urbdial.divnot'):
    translation_domain = getUtility(ITranslationDomain, domain)
    properties = api.portal.get_tool('portal_properties')
    target_language = properties.site_properties.default_language

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


def get_display_values(values, voc_name, context=None, separator=None):
    voc_factory = queryUtility(IVocabularyFactory, voc_name)
    voc = voc_factory(context)
    display_values = [voc.getTerm(val).title for val in values]

    if separator is not None:
        display_values = separator.join(display_values)

    return display_values
