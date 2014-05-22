# -*- coding: utf-8 -*-

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

        vocabulary_terms = []
        for postal_code, locality in localities.value.iteritems():
            postal_code = postal_code.encode('utf-8')
            vocabulary_terms.append(
                SimpleTerm(postal_code, postal_code, locality)
            )

        # Sort values alphabetically
        vocabulary_terms = sorted(vocabulary_terms, key=lambda term: term.title)
        vocabulary = SimpleVocabulary(vocabulary_terms)
        return vocabulary
