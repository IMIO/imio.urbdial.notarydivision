# -*- coding: utf-8 -*-

from Products.CMFPlone.utils import normalizeString

from plone import api

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class LocalitiesVocabularyFactory(object):
    """
    Vocabulary factory for localities
    """

    def __call__(self, context):
        registry = api.portal.get_tool('portal_registry')
        localities = registry.records.get('imio.urbdial.notarydivision.localities')

        vocabulary = []
        for term in localities.value:
            vocabulary.append(
                SimpleTerm(
                    term,
                    normalizeString(term),
                    term,
                )
            )
        vocabulary = SimpleVocabulary(vocabulary)
        return vocabulary
