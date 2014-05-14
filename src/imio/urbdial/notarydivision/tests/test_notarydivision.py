# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from Acquisition import aq_base

from plone import api

from imio.urbdial.notarydivision.testing import BrowserTest
from imio.urbdial.notarydivision.testing import EXAMPLE_DIVISION_INTEGRATION
from imio.urbdial.notarydivision.testing import TEST_INSTALL_INTEGRATION

from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD

import unittest


class TestInstall(unittest.TestCase):
    """
    Test installation of imio.urbdial.notarydivision into Plone.
    """

    layer = TEST_INSTALL_INTEGRATION

    def test_portal_type_is_registered(self):
        portal_types = api.portal.get_tool('portal_types')
        registered_types = portal_types.listContentTypes()
        self.assertTrue('NotaryDivision' in registered_types)

    def test_creation_permission_is_addNotaryDivision(self):
        portal_types = api.portal.get_tool('portal_types')
        divnot_type = portal_types.NotaryDivision
        self.assertTrue(divnot_type.add_permission == 'imio.urbdial.notarydivision.AddNotaryDivision')


class TestNotaryDivisionFields(unittest.TestCase):
    """
    Test schema fields declaration.
    """

    layer = EXAMPLE_DIVISION_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.test_divnot = aq_base(self.portal.notarydivisions.objectValues()[0])

    def test_class_registration(self):
        from imio.urbdial.notarydivision.content.NotaryDivision import NotaryDivision
        self.assertTrue(self.test_divnot.__class__ == NotaryDivision)

    def test_schema_registration(self):
        portal_types = api.portal.get_tool('portal_types')
        divnot_type = portal_types.get(self.test_divnot.portal_type)
        self.assertTrue('INotaryDivision' in divnot_type.schema)

    def test_exclude_from_navigation_field(self):
        self.assertTrue(hasattr(self.test_divnot, 'exclude_from_nav'))

    def test_exclude_from_navigation_field_default_value_is_True(self):
        self.assertTrue(self.test_divnot.exclude_from_nav)

    def test_Reference_field_declaration(self):
        self.assertTrue(hasattr(self.test_divnot, 'reference'))

    def test_Applicants_field_declaration(self):
        self.assertTrue(hasattr(self.test_divnot, 'applicants'))


class TestNotaryDivisionInBrowser(BrowserTest):
    """
    Test NotaryDivision behavior in a browser.
    """

    layer = EXAMPLE_DIVISION_INTEGRATION

    def setUp(self):
        super(TestNotaryDivisionInBrowser, self).setUp()
        self.test_divnot = self.portal.notarydivisions.objectValues()[0]
        self.browserLogin(TEST_USER_NAME, TEST_USER_PASSWORD)

    def test_NotaryDivision_excluded_from_navigation(self):
        self.browser.open(self.portal.absolute_url())
        contents = self.browser.contents
        msg = 'test NotaryDivision appears in navigation bar'
        self.assertTrue('<li id="portaltab-test_notarydivision" class="plain">' not in contents, msg)

    def test_exclude_from_navigation_field_is_hidden(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = 'field exclude_from_nav should be hidden in Display View'
        self.assertTrue('<span id="form-widgets-exclude_from_nav"' not in contents, msg)
