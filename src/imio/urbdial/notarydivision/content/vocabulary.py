# -*- coding: utf-8 -*-

from Products.PlonePAS.tools.groupdata import GroupData

from Products.CMFPlone.utils import normalizeString

from imio.urbdial.notarydivision.utils import get_notary_groups
from imio.urbdial.notarydivision.utils import translate as _

from plone import api

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class NotaryOfficeVocabularyFactory(object):
    """
    Vocabulary for the notary offices: all subgroups of notaries group.
    """

    def __call__(self, context):
        notary_group = api.group.get('notaries')
        # get all subgroups of notaries group
        notary_office_groups = [g for g in notary_group.getAllGroupMembers() if isinstance(g, GroupData)]

        vocabulary_terms = []
        for group in notary_office_groups:
            vocabulary_terms.append(
                SimpleTerm(group.id, group.id, group.getProperty('title'))
            )

        vocabulary = SimpleVocabulary(vocabulary_terms)
        return vocabulary


class LocalNotariesVocabularyFactory(object):
    """
    Return a vocabulary of all notaries in the same notary office than the field 'notary_office'
    of the notarydivision or the same notary office than the current user.
    """

    def __call__(self, context):
        # to implement

        notary_offices = getattr(context, 'notary_office', None)
        # in case of add form, the notary_office field is not assigned yet
        if notary_offices is None:
            current_user = api.user.get_current()
            notary_office_groups = get_notary_groups(current_user)
        else:
            notary_office_groups = [api.group.get(name) for name in notary_offices]

        local_notaries = self._get_users_from_groups(notary_office_groups)
        vocabulary_terms = []
        for notary in local_notaries:
            vocabulary_terms.append(
                SimpleTerm(notary.id, notary.id, notary.getProperty('fullname'))
            )

        vocabulary = SimpleVocabulary(vocabulary_terms)
        return vocabulary

    def _get_users_from_groups(self, group_list):
        all_users = []
        for group in group_list:
            group_users = group.getGroupMembers()
            all_users.extend(group_users)

        return all_users


class DGO4VocabularyFactory(object):
    """
    Vocabulary for the DGO4's: all subgroups of dgo4 group.
    """

    def __call__(self, context):
        dgo4_group = api.group.get('dgo4')
        # get all subgroups of dgo4 group
        local_dgo4_groups = [g for g in dgo4_group.getAllGroupMembers() if isinstance(g, GroupData)]

        vocabulary_terms = []
        for group in local_dgo4_groups:
            vocabulary_terms.append(
                SimpleTerm(group.id, group.id, group.getProperty('title'))
            )

        vocabulary = SimpleVocabulary(vocabulary_terms)
        return vocabulary


class TownshipVocabularyFactory(object):
    """
    Vocabulary for the townships: all subgroups of townships group.
    """

    def __call__(self, context):
        townships_group = api.group.get('townships')
        # get all subgroups of townships group
        local_township_groups = [g for g in townships_group.getAllGroupMembers() if isinstance(g, GroupData)]

        vocabulary_terms = []
        for group in local_township_groups:
            vocabulary_terms.append(
                SimpleTerm(group.id, group.id, group.getProperty('title'))
            )

        vocabulary = SimpleVocabulary(vocabulary_terms)
        return vocabulary


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


class CededVocabularyFactory(object):
    """
    Vocabulary factory for article ceded parcellings options.
    """

    def __call__(self, context):

        vocabulary_terms = [
            SimpleTerm(True, 'yes', _('Ceded parcelling')),
            SimpleTerm(False, 'no', _('Kept parcelling'))
        ]

        vocabulary = SimpleVocabulary(vocabulary_terms)
        return vocabulary
