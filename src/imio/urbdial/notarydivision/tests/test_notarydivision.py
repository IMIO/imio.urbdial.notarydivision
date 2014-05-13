# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from plone import api

from imio.urbdial.notarydivision.testing import IntegrationTestCase


class TestInstall(IntegrationTestCase):
    """Test installation of imio.urbdial.notarydivision into Plone."""

    def test_portal_type_is_registered(self):
        portal_types = api.portal.get_tool('portal_types')
        registered_types = portal_types.listContentTypes()
        self.assertTrue('NotaryDivision' in registered_types)

    def test_creation_permission_is_addNotaryDivision(self):
        """
        """
        portal_types = api.portal.get_tool('portal_types')
        divnot_type = portal_types.NotaryDivision
        self.assertTrue(divnot_type.add_permission == 'imio.urbdial.notarydivision.AddNotaryDivision')


class TestNotaryDivisionFields(IntegrationTestCase):
    """
    Test schema fields declaration
    """

    def setUp(self):
        self.portal = self.layer['portal']

        # create a test NotaryDivision
        self.divnot = api.content.create(
            type='NotaryDivision',
            id='test_notarydivision',
            container=self.portal.notarydivisions,
        )

    def test_class_registration(self):
        from imio.urbdial.notarydivision.content.NotaryDivision import NotaryDivision
        self.assertTrue(self.divnot.__class__ == NotaryDivision)

    def test_schema_registration(self):
        portal_types = api.portal.get_tool('portal_types')
        divnot_type = portal_types.get(self.divnot.portal_type)
        self.assertTrue('INotaryDivision' in divnot_type.schema)
