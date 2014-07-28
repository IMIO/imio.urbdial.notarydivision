# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.testing import TEST_INSTALL_INTEGRATION

from plone import api

import unittest


class TestInitialParcel(unittest.TestCase):
    """
    Test portal_types install.
    """

    layer = TEST_INSTALL_INTEGRATION

    def test_InitialParcel_portal_type_is_registered(self):
        portal_types = api.portal.get_tool('portal_types')
        registered_types = portal_types.listContentTypes()
        self.assertTrue('InitialParcel' in registered_types)

    def test_creation_permission_is_AddParcel(self):
        portal_types = api.portal.get_tool('portal_types')
        parcel_type = portal_types.InitialParcel
        self.assertTrue(parcel_type.add_permission == 'imio.urbdial.notarydivision.AddParcel')


class TestCreatedParcel(unittest.TestCase):
    """
    Test portal_types install.
    """

    layer = TEST_INSTALL_INTEGRATION

    def test_CreatedParcel_portal_type_is_registered(self):
        portal_types = api.portal.get_tool('portal_types')
        registered_types = portal_types.listContentTypes()
        self.assertTrue('CreatedParcel' in registered_types)

    def test_creation_permission_is_AddParcel(self):
        portal_types = api.portal.get_tool('portal_types')
        parcel_type = portal_types.CreatedParcel
        self.assertTrue(parcel_type.add_permission == 'imio.urbdial.notarydivision.AddParcel')
