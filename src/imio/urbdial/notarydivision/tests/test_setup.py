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
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_dexterity_is_dependency_of_urbdial(self):
        """
        Dexterity should be installed when we install urbdial
        """
        self.assertTrue(not self.installer.isProductInstalled('plone.app.dexterity'))
        applyProfile(self.portal, 'imio.urbdial.notarydivision:testing')
        self.assertTrue(self.installer.isProductInstalled('plone.app.dexterity'))


class TestInstall(IntegrationTestCase):
    """
    Test installation of imio.urbdial.notarydivision into Plone.
    """

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """
        Test if imio.urbdial.notarydivision is installed with portal_quickinstaller.
        """
        self.assertTrue(self.installer.isProductInstalled('imio.urbdial.notarydivision'))

    def test_uninstall(self):
        """
        Test if imio.urbdial.notarydivision is cleanly uninstalled.
        """
        self.installer.uninstallProducts(['imio.urbdial.notarydivision'])
        self.assertTrue(not self.installer.isProductInstalled('imio.urbdial.notarydivision'))

    def test_browserlayer(self):
        """
        Test that IImioUrbdialNotarydivisionLayer is registered.
        """
        from imio.urbdial.notarydivision.interfaces import IImioUrbdialNotarydivisionLayer
        from plone.browserlayer import utils
        self.assertIn(IImioUrbdialNotarydivisionLayer, utils.registered_layers())


class TestSetup(unittest.TestCase):
    """
    Test custom code of setuphandlers.py.
    """

    layer = NAKED_PLONE_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        # apply plone default profile so we have default workflows on plone
        # content types and we can run the next import step without troubles
        applyProfile(self.portal, 'Products.CMFPlone:plone')
        # create plone root default objects
        applyProfile(self.portal, 'Products.CMFPlone:plone-content')
        # install urbdial.notarydivision
        applyProfile(self.portal, 'imio.urbdial.notarydivision:testing')

    def test_plone_root_default_objects_deleted(self):
        """
        We have to get rid of plone root default objects.
        """
        root_object_ids = self.portal.objectIds()
        self.assertTrue('news' not in root_object_ids)
        self.assertTrue('events' not in root_object_ids)
        self.assertTrue('front-page' not in root_object_ids)
        self.assertTrue('Members' not in root_object_ids)

    def test_notarydivisions_folder_created(self):
        """
        """
        self.assertTrue('notarydivisions' in self.portal.objectIds())
        divnot_folder = self.portal.notarydivisions
        self.assertTrue(divnot_folder.portal_type == 'Folder')

    def test_notarydivisions_folder_allowed_types(self):
        """
        The notarydivisions folder should only contains NotaryDivision objects.
        """
        portal_types = api.portal.get_tool('portal_types')
        divnot_type = portal_types.notarydivision
        divnot_folder = self.portal.notarydivisions
        allowed_types = divnot_folder.allowedContentTypes()
        self.assertTrue(len(allowed_types) == 1)
        self.assertTrue(divnot_type in allowed_types)
