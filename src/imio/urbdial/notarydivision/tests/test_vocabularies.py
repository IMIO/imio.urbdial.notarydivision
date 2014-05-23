# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.testing import TEST_INSTALL_INTEGRATION

from plone import api

from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

import unittest


class TestVocabularies(unittest.TestCase):

    layer = TEST_INSTALL_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = api.portal.get_tool('portal_registry')

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
