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


class TestInitialParcelView(NotaryDivisionBrowserTest):
    """
    """

    def test_InitialParcelView_class_registration(self):
        from imio.urbdial.notarydivision.content.parcel_view import ParcelView
        view = self.test_initialparcel.restrictedTraverse('view')
        self.assertTrue(isinstance(view, ParcelView))

    def test_InitialParcel_view_redirects_to_NotaryDivisionView(self):
        self.browser.open(self.test_initialparcel.absolute_url())
        notary_division_url = self.test_divnot.absolute_url()
        msg = 'InitialParcel view does not redirect to NotaryDivisionView'
        self.assertTrue(self.browser.url == notary_division_url + '/view#initial_estate', msg)


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

    def test_initial_parcel_add_form_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "Inital parcel add form is not visible on notary division"
        self.assertTrue('kssattr-formname-InitialParcel' in contents, msg)

    def test_locality_attribute(self):
        test_initialparcel = aq_base(self.test_initialparcel)
        self.assertTrue(hasattr(test_initialparcel, 'locality'))

    def test_locality_field_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "field 'locality' is not displayed"
        self.assertTrue('id="form-widgets-locality"' in contents, msg)
        msg = "field 'locality' is not translated"
        self.assertTrue('' in contents, msg)

    def test_locality_field_edit(self):
        self.browser.open(self.test_initialparcel.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'locality' is not editable"
        self.assertTrue('Commune' in contents, msg)

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
