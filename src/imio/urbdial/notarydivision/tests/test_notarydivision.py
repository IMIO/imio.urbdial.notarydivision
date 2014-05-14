# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from plone import api

from imio.urbdial.notarydivision.testing import EXAMPLE_DIVISION_INTEGRATION
from imio.urbdial.notarydivision.testing import TEST_INSTALL_INTEGRATION

import unittest


class TestInstall(unittest.TestCase):
    """Test installation of imio.urbdial.notarydivision into Plone."""

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
    Test schema fields declaration
    """

    layer = EXAMPLE_DIVISION_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.divnot = self.portal.notarydivisions.objectValues()[0]

    def test_class_registration(self):
        from imio.urbdial.notarydivision.content.NotaryDivision import NotaryDivision
        self.assertTrue(self.divnot.__class__ == NotaryDivision)

    def test_schema_registration(self):
        portal_types = api.portal.get_tool('portal_types')
        divnot_type = portal_types.get(self.divnot.portal_type)
        self.assertTrue('INotaryDivision' in divnot_type.schema)

    def test_Reference_field_declaration(self):
        self.assertTrue(hasattr(self.divnot, 'reference'))

    def test_Applicants_field_declaration(self):
        self.assertTrue(hasattr(self.divnot, 'applicants'))
