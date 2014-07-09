# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.testing import TEST_INSTALL_INTEGRATION
from imio.urbdial.notarydivision.vars import DGO4_LOCAL_GROUPS
from imio.urbdial.notarydivision.vars import TOWNSHIPS_LOCAL_GROUPS

from plone import api

from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

import unittest


class TestVocabularies(unittest.TestCase):

    layer = TEST_INSTALL_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = api.portal.get_tool('portal_registry')

    def test_dgo4s_vocabulary_factory_registration(self):
        """
        dgo4s voc factory should be registered as a named utility.
        """
        factory_name = 'imio.urbdial.notarydivision.dgo4s'
        self.assertTrue(queryUtility(IVocabularyFactory, factory_name))

    def test_dgo4s_vocabulary_values(self):
        """
        dgo4s should be sorted on title.
        """
        factory_name = 'imio.urbdial.notarydivision.dgo4s'
        dgo4s_voc_factory = queryUtility(IVocabularyFactory, factory_name)

        dgo4s = dgo4s_voc_factory(self.portal)
        dgo4s_titles = [term.title for term in dgo4s]
        expected_titles = [group['title'] for group in DGO4_LOCAL_GROUPS]
        msg = "some dgo4 local groups are not found in dgo4s vocabulary"
        self.assertTrue(set(expected_titles) == set(dgo4s_titles), msg)

    def test_townships_vocabulary_factory_registration(self):
        """
        townships voc factory should be registered as a named utility.
        """
        factory_name = 'imio.urbdial.notarydivision.townships'
        self.assertTrue(queryUtility(IVocabularyFactory, factory_name))

    def test_townships_vocabulary_values(self):
        """
        townships should be sorted on title.
        """
        factory_name = 'imio.urbdial.notarydivision.townships'
        townships_voc_factory = queryUtility(IVocabularyFactory, factory_name)

        townships = townships_voc_factory(self.portal)
        townships_titles = [term.title for term in townships]
        expected_titles = [group['title'] for group in TOWNSHIPS_LOCAL_GROUPS]
        msg = "some township local groups are not found in townships vocabulary"
        self.assertTrue(set(expected_titles) == set(townships_titles), msg)

    def test_localities_vocabulary_registration(self):
        """
        Localities defined in registry.xml should be available in
        portal_registry after installation.
        """
        voc_name = 'imio.urbdial.notarydivision.localities'
        msg = 'Localities are not loaded in the registry'
        self.assertTrue(voc_name in self.registry.records, msg)

    def test_localities_vocabulary_values(self):
        """
        Test some localities values.
        """
        voc_name = 'imio.urbdial.notarydivision.localities'
        record = self.registry.records.get(voc_name)
        localities = record.value.values()
        self.assertTrue(u'Aiseau-Presles' in localities)
        self.assertTrue(u'Namur' in localities)
        self.assertTrue(u'Wanze' in localities)

    def test_localities_vocabulary_factory_registration(self):
        """
        Localities voc factory should be registered as a named utility.
        """
        factory_name = 'imio.urbdial.notarydivision.Localities'
        self.assertTrue(queryUtility(IVocabularyFactory, factory_name))

    def test_localities_vocabulary_is_sorted_on_title(self):
        """
        Localities should be sorted on title.
        """
        factory_name = 'imio.urbdial.notarydivision.Localities'
        localities_voc_factory = queryUtility(IVocabularyFactory, factory_name)

        localities = localities_voc_factory(self.portal)
        localities_title = [term.title for term in localities]
        self.assertTrue(localities_title == sorted(localities_title))

    def test_surface_accuracy_vocabulary_registration(self):
        """
        Surface accuracies defined in registry.xml should be available in
        portal_registry after installation.
        """
        voc_name = 'imio.urbdial.notarydivision.surface_accuracies'
        msg = 'Surface accuracies are not loaded in the registry'
        self.assertTrue(voc_name in self.registry.records, msg)

    def test_surface_accuracy_vocabulary_values(self):
        """
        Test some surface_accuracy values.
        """
        voc_name = 'imio.urbdial.notarydivision.surface_accuracies'
        record = self.registry.records.get(voc_name)
        surface_accuracies = record.value
        self.assertTrue(u'cadastrale' in surface_accuracies)
        self.assertTrue(u'mesurée' in surface_accuracies)

    def test_surface_accuracy_vocabulary_factory_registration(self):
        """
        Surface accuracies voc factory should be registered as a named utility.
        """
        factory_name = 'imio.urbdial.notarydivision.SurfaceAccuracies'
        self.assertTrue(queryUtility(IVocabularyFactory, factory_name))

    def test_deed_type_vocabulary_registration(self):
        """
        Deed types defined in registry.xml should be available in
        portal_registry after installation.
        """
        voc_name = 'imio.urbdial.notarydivision.deed_types'
        msg = 'Deed types are not loaded in the registry'
        self.assertTrue(voc_name in self.registry.records, msg)

    def test_deed_type_vocabulary_values(self):
        """
        Test some deed_type values.
        """
        voc_name = 'imio.urbdial.notarydivision.deed_types'
        record = self.registry.records.get(voc_name)
        deed_types = record.value
        self.assertTrue(u"vente" in deed_types)
        self.assertTrue(u"droit d'emphytéose" in deed_types)

    def test_deed_type_vocabulary_factory_registration(self):
        """
        Deed types voc factory should be registered as a named utility.
        """
        factory_name = 'imio.urbdial.notarydivision.DeedTypes'
        self.assertTrue(queryUtility(IVocabularyFactory, factory_name))

    def test_article_90_vocabulary_registration(self):
        """
        Reasons for article 90 vocabulary defined in registry.xml
        should be available in portal_registry after installation.
        """
        voc_name = 'imio.urbdial.notarydivision.article_90_reasons'
        msg = 'Article 90 reaons are not loaded in the registry'
        self.assertTrue(voc_name in self.registry.records, msg)

    def test_article_90_vocabulary_values(self):
        """
        Test some article_90 values.
        """
        voc_name = 'imio.urbdial.notarydivision.article_90_reasons'
        record = self.registry.records.get(voc_name)
        reasons = record.value
        self.assertTrue(u"1° : la division résulte d'un ou plusieurs acte(s) de donation" in reasons)
        self.assertTrue(u"2° : la division résulte d'un ou plusieurs acte(s) involontaire(s)" in reasons)

    def test_article_90_vocabulary_factory_registration(self):
        """
        Article 90 reasons voc factory should be registered as a named utility.
        """
        factory_name = 'imio.urbdial.notarydivision.Article90Reasons'
        self.assertTrue(queryUtility(IVocabularyFactory, factory_name))
