# -*- coding: utf-8 -*-

from Products.CMFPlone.utils import normalizeString

from imio.urbdial.notarydivision.utils import translate as _

from plone import api

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class LocalitiesVocabularyFactory(object):
    """
    Vocabulary factory for localities.
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


class SurfaceAccuraciesVocabularyFactory(object):
    """
    Vocabulary factory for surface accuracy.
    """

    def __call__(self, context):
        registry = api.portal.get_tool('portal_registry')
        accuracies = registry.records.get('imio.urbdial.notarydivision.surface_accuracies')

        vocabulary_terms = []
        for accuracy in accuracies.value:
            term_key = normalizeString(accuracy)
            vocabulary_terms.append(
                SimpleTerm(term_key, term_key, _(accuracy))
            )

        vocabulary = SimpleVocabulary(vocabulary_terms)
        return vocabulary


class DeedTypesVocabularyFactory(object):
    """
    Vocabulary factory for deed types.
    """

    def __call__(self, context):
        registry = api.portal.get_tool('portal_registry')
        deed_types = registry.records.get('imio.urbdial.notarydivision.deed_types')

        vocabulary_terms = []
        for deed_type in deed_types.value:
            term_key = normalizeString(deed_type)
            vocabulary_terms.append(
                SimpleTerm(term_key, term_key, _(deed_type))
            )

        vocabulary = SimpleVocabulary(vocabulary_terms)
        return vocabulary


class Article90VocabularyFactory(object):
    """
    Vocabulary factory for article 90 reasons.
    """

    def __call__(self, context):
        registry = api.portal.get_tool('portal_registry')
        reasons = registry.records.get('imio.urbdial.notarydivision.article_90_reasons')

        vocabulary_terms = []
        for reason in reasons.value:
            term_key = normalizeString(reason[:3])
            vocabulary_terms.append(
                SimpleTerm(term_key, term_key, _(reason))
            )

        vocabulary = SimpleVocabulary(vocabulary_terms)
        return vocabulary
