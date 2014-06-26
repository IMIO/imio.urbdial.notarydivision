# -*- coding: utf-8 -*-

from zope.component import getUtility
from zope.i18n.interfaces import ITranslationDomain


def translate(msgid, domain='urbdial.divnot'):
    translation_domain = getUtility(ITranslationDomain, domain)
    return translation_domain.translate(msgid, target_language='fr', default=msgid)
