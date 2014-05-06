# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from imio.urbdial.notarydivision.testing import IntegrationTestCase
from imio.urbdial.notarydivision.testing import NAKED_PLONE_INTEGRATION
from plone.app.testing import applyProfile
from plone import api
import unittest


class TestInstallDependencies(unittest.TestCase):

    layer = NAKED_PLONE_INTEGRATION

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_dexterity_is_dependency_of_urbdial(self):
        self.assertTrue(not self.installer.isProductInstalled('plone.app.dexterity'))
        applyProfile(self.portal, 'imio.urbdial.notarydivision:testing')
        self.assertTrue(self.installer.isProductInstalled('plone.app.dexterity'))


class TestInstall(IntegrationTestCase):
    """Test installation of imio.urbdial.notarydivision into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if imio.urbdial.notarydivision is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('imio.urbdial.notarydivision'))

    def test_uninstall(self):
        """Test if imio.urbdial.notarydivision is cleanly uninstalled."""
        self.installer.uninstallProducts(['imio.urbdial.notarydivision'])
        self.assertTrue(not self.installer.isProductInstalled('imio.urbdial.notarydivision'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IImioUrbdialNotarydivisionLayer is registered."""
        from imio.urbdial.notarydivision.interfaces import IImioUrbdialNotarydivisionLayer
        from plone.browserlayer import utils
        self.assertIn(IImioUrbdialNotarydivisionLayer, utils.registered_layers())


class TestSetup(IntegrationTestCase):
    """ Test custom code of setuphandlers.py. """

    def setUp(self):
        self.portal = self.layer['portal']
        # apply plone default profile so we have default workflows on plone
        # content types and we can run the next import step without troubles
        applyProfile(self.portal, 'Products.CMFPlone:plone')
        # create plone root default objects
        applyProfile(self.portal, 'Products.CMFPlone:plone-content')

    def test_plone_root_default_objects_deleted(self):
        root_object_ids = self.portal.objectIds()
        self.assertTrue('news' not in root_object_ids)
        self.assertTrue('events' not in root_object_ids)
        self.assertTrue('front-page' not in root_object_ids)
        self.assertTrue('Members' not in root_object_ids)
