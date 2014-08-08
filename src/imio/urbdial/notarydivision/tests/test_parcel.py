# -*- coding: utf-8 -*-

from Acquisition import aq_base

from imio.urbdial.notarydivision.testing import TEST_INSTALL_INTEGRATION
from imio.urbdial.notarydivision.testing import NotaryDivisionBrowserTest

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


class TestInitialParcelFields(NotaryDivisionBrowserTest):
    """
    Test schema fields declaration.
    """

    def test_class_registration(self):
        from imio.urbdial.notarydivision.content.parcel import InitialParcel
        self.assertTrue(self.test_initialparcel.__class__ == InitialParcel)

    def test_schema_registration(self):
        portal_types = api.portal.get_tool('portal_types')
        parcel_type = portal_types.get(self.test_initialparcel.portal_type)
        self.assertTrue('IInitialParcel' in parcel_type.schema)

    def test_locality_attribute(self):
        test_initialparcel = aq_base(self.test_initialparcel)
        self.assertTrue(hasattr(test_initialparcel, 'locality'))

    def test_division_attribute(self):
        test_initialparcel = aq_base(self.test_initialparcel)
        self.assertTrue(hasattr(test_initialparcel, 'division'))

    def test_section_attribute(self):
        test_initialparcel = aq_base(self.test_initialparcel)
        self.assertTrue(hasattr(test_initialparcel, 'section'))

    def test_radical_attribute(self):
        test_initialparcel = aq_base(self.test_initialparcel)
        self.assertTrue(hasattr(test_initialparcel, 'radical'))

    def test_bis_attribute(self):
        test_initialparcel = aq_base(self.test_initialparcel)
        self.assertTrue(hasattr(test_initialparcel, 'bis'))

    def test_exposant_attribute(self):
        test_initialparcel = aq_base(self.test_initialparcel)
        self.assertTrue(hasattr(test_initialparcel, 'exposant'))

    def test_power_attribute(self):
        test_initialparcel = aq_base(self.test_initialparcel)
        self.assertTrue(hasattr(test_initialparcel, 'power'))

    def test_surface_attribute(self):
        test_initialparcel = aq_base(self.test_initialparcel)
        self.assertTrue(hasattr(test_initialparcel, 'surface'))

    def test_undivided_attribute(self):
        test_initialparcel = aq_base(self.test_initialparcel)
        self.assertTrue(hasattr(test_initialparcel, 'undivided_a'))

    def test_specific_rights_attribute(self):
        test_initialparcel = aq_base(self.test_initialparcel)
        self.assertTrue(hasattr(test_initialparcel, 'specific_rights_a'))


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


class TestCreatedParcelFields(NotaryDivisionBrowserTest):
    """
    Test schema fields declaration.
    """

    def test_class_registration(self):
        from imio.urbdial.notarydivision.content.parcel import CreatedParcel
        self.assertTrue(self.test_createdparcel.__class__ == CreatedParcel)

    def test_schema_registration(self):
        portal_types = api.portal.get_tool('portal_types')
        parcel_type = portal_types.get(self.test_createdparcel.portal_type)
        self.assertTrue('ICreatedParcel' in parcel_type.schema)

    def test_undivided_attribute(self):
        test_createdparcel = aq_base(self.test_createdparcel)
        self.assertTrue(hasattr(test_createdparcel, 'undivided_b'))

    def test_specific_rights_attribute(self):
        test_createdparcel = aq_base(self.test_createdparcel)
        self.assertTrue(hasattr(test_createdparcel, 'specific_rights_b'))

    def test_surface_attribute(self):
        test_createdparcel = aq_base(self.test_createdparcel)
        self.assertTrue(hasattr(test_createdparcel, 'surface'))

    def test_surface_accuracy_attribute(self):
        test_createdparcel = aq_base(self.test_createdparcel)
        self.assertTrue(hasattr(test_createdparcel, 'surface_accuracy'))

    def test_built_attribute(self):
        test_createdparcel = aq_base(self.test_createdparcel)
        self.assertTrue(hasattr(test_createdparcel, 'built'))

    def test_deed_type_attribute(self):
        test_createdparcel = aq_base(self.test_createdparcel)
        self.assertTrue(hasattr(test_createdparcel, 'deed_type'))

    def test_destination_attribute(self):
        test_createdparcel = aq_base(self.test_createdparcel)
        self.assertTrue(hasattr(test_createdparcel, 'destination'))
