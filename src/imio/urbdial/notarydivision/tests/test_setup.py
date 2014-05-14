# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from imio.urbdial.notarydivision.testing import NAKED_PLONE_INTEGRATION
from imio.urbdial.notarydivision.testing import REAL_INSTALL_INTEGRATION
from imio.urbdial.notarydivision.testing import TEST_INSTALL_INTEGRATION

from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.testing import applyProfile

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

    def test_z3cformDataGridField_is_dependency_of_urbdial(self):
        """
        Collective.z3cform.datagridfield should be installed when we install urbdial
        """
        self.assertTrue(not self.installer.isProductInstalled('collective.z3cform.datagridfield'))
        applyProfile(self.portal, 'imio.urbdial.notarydivision:testing')
        self.assertTrue(self.installer.isProductInstalled('collective.z3cform.datagridfield'))


class TestInstall(unittest.TestCase):
    """
    Test installation of imio.urbdial.notarydivision into Plone.
    """

    layer = TEST_INSTALL_INTEGRATION

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

    layer = REAL_INSTALL_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']

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

    def test_notarydivisions_folder_translation(self):
        """
        """
        divnot_folder = self.portal.notarydivisions
        self.assertTrue(divnot_folder.Title() == 'Divisions notariales')

    def test_notarydivisions_folder_allowed_types(self):
        """
        The notarydivisions folder should only contains NotaryDivision objects.
        """
        portal_types = api.portal.get_tool('portal_types')
        divnot_type = portal_types.NotaryDivision
        divnot_folder = self.portal.notarydivisions
        allowed_types = divnot_folder.allowedContentTypes()
        self.assertTrue(len(allowed_types) == 1)
        self.assertTrue(divnot_type in allowed_types)

    def test_notarydivisions_folder_Reader_local_role(self):
        """
        Members of group 'notaries' should have the local role 'Reader' on that folder
        """
        divnot_folder = self.portal.notarydivisions
        folder_local_roles = dict(divnot_folder.get_local_roles())
        self.assertTrue(u'Reader' in folder_local_roles['notaries'])

    def test_notarydivisions_folder_NotaryDivisionCreator_local_role(self):
        """
        Members of group 'notaries' should have the local role 'NotaryDivision Creator' on that folder
        """
        divnot_folder = self.portal.notarydivisions
        folder_local_roles = dict(divnot_folder.get_local_roles())
        self.assertTrue(u'NotaryDivision Creator' in folder_local_roles['notaries'])

    def test_notarydivisions_folder_provides_INavigationRoot(self):
        """
        """
        divnot_folder = self.portal.notarydivisions
        self.assertTrue(INavigationRoot.providedBy(divnot_folder))
