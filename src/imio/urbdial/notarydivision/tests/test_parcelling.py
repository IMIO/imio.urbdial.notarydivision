# -*- coding: utf-8 -*-

from Acquisition import aq_base

from imio.urbdial.notarydivision.testing import TEST_INSTALL_INTEGRATION
from imio.urbdial.notarydivision.testing import NotaryDivisionBrowserTest
from imio.urbdial.notarydivision.testing import NotaryDivisionFunctionalBrowserTest

from plone import api

import transaction

import unittest


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


class TestCreatedParcelView(NotaryDivisionBrowserTest):
    """
    Test CreatedParcel view
    """

    def test_CreatedParcelView_class_registration(self):
        from imio.urbdial.notarydivision.content.parcel_view import ParcelView
        view = self.test_parcelling.restrictedTraverse('view')
        self.assertTrue(isinstance(view, ParcelView))

    def test_CreatedParcel_view_redirects_to_NotaryDivisionView(self):
        self.browser.open(self.test_parcelling.absolute_url())
        notary_division_url = self.test_divnot.absolute_url()
        msg = 'CreatedParcel view does not redirect to NotaryDivisionView'
        self.assertTrue(self.browser.url == notary_division_url + '/#fieldset-estate', msg)


class TestCreatedParcelAddForm(NotaryDivisionFunctionalBrowserTest):
    """
    Test CreatedParcel add form
    """

    def test_created_parcel_add_form_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "Inital parcel add form is not visible on notary division"
        self.assertTrue('kssattr-formname-CreatedParcel' in contents, msg)

    def test_parcel_number_autoincrement_starting_value(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "Default created parcel number should be 1"
        self.assertTrue('autoincrementint-field" value="1"' in contents, msg)

    def test_parcel_number_autoincrement_value(self):
        """
        Set test CreatedParcel number to 1 => the lowest number available is now '2'
        """
        self.test_parcelling.number = 1
        transaction.commit()
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "Default created parcel number should be 2"
        self.assertTrue('autoincrementint-field" value="2"' in contents, msg)

    def test_parcel_number_autoincrement_deleted_value(self):
        """
        Set test CreatedParcel number to 1 and create an CreatedParcel with number 2 => the
        next proposed number should be 3 but if we delete the first parcel, then number '1'
        is 'free' again and should be proposed as default number.
        """
        self.test_parcelling.number = 1
        api.content.create(type='CreatedParcel', id='parcel2', container=self.test_divnot, number=2)
        transaction.commit()
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "Default created parcel number should be 3"
        self.assertTrue('autoincrementint-field" value="3"' in contents, msg)

        # delete the number 1 created parcel => the lowest available number become '1' again
        api.content.delete(self.test_parcelling)
        transaction.commit()
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "Default created parcel number should be 1"
        self.assertTrue('autoincrementint-field" value="1"' in contents, msg)
        self.assertTrue('autoincrementint-field" value="3"' not in contents, msg)


class TestCreatedParcelFields(NotaryDivisionBrowserTest):
    """
    Test schema fields declaration.
    """

    def test_class_registration(self):
        from imio.urbdial.notarydivision.content.parcel import CreatedParcel
        self.assertTrue(self.test_parcelling.__class__ == CreatedParcel)

    def test_schema_registration(self):
        portal_types = api.portal.get_tool('portal_types')
        parcel_type = portal_types.get(self.test_parcelling.portal_type)
        self.assertTrue('ICreatedParcel' in parcel_type.schema)

    def test_undivided_attribute(self):
        test_parcelling = aq_base(self.test_parcelling)
        self.assertTrue(hasattr(test_parcelling, 'undivided_b'))

    def test_undivided_field_edit(self):
        self.browser.open(self.test_parcelling.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'undivided' is not editable"
        self.assertTrue('En cas d’indivision ou de démembrement' in contents, msg)

    def test_specific_rights_attribute(self):
        test_parcelling = aq_base(self.test_parcelling)
        self.assertTrue(hasattr(test_parcelling, 'specific_rights_b'))

    def test_surface_accuracy_attribute(self):
        test_parcelling = aq_base(self.test_parcelling)
        self.assertTrue(hasattr(test_parcelling, 'surface_accuracy'))

    def test_bis_field_edit(self):
        self.browser.open(self.test_parcelling.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'bis' is not editable"
        self.assertTrue('Bis' in contents, msg)

    def test_road_distance_attribute(self):
        test_parcelling = aq_base(self.test_parcelling)
        self.assertTrue(hasattr(test_parcelling, 'road_distance'))

    def test_surfaceaccuracy_field_edit(self):
        self.browser.open(self.test_parcelling.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'surfaceaccuracy' is not editable"
        self.assertTrue('cadastrale' in contents, msg)

    def test_built_attribute(self):
        test_parcelling = aq_base(self.test_parcelling)
        self.assertTrue(hasattr(test_parcelling, 'built'))

    def test_built_field_edit(self):
        self.browser.open(self.test_parcelling.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'built' is not editable"
        self.assertTrue('Bâti' in contents, msg)

    def test_deed_type_attribute(self):
        test_parcelling = aq_base(self.test_parcelling)
        self.assertTrue(hasattr(test_parcelling, 'deed_type'))

    def test_deedtype_field_edit(self):
        self.browser.open(self.test_parcelling.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'deedtype' is not editable"
        self.assertTrue("Type d'acte" in contents, msg)

    def test_other_deed_type_attribute(self):
        test_parcelling = aq_base(self.test_parcelling)
        self.assertTrue(hasattr(test_parcelling, 'other_deed_type'))

    def test_otherdeedtype_field_edit(self):
        self.browser.open(self.test_parcelling.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'otherdeedtype' is not editable"
        self.assertTrue("Autre type d'acte" in contents, msg)

    def test_destination_attribute(self):
        test_parcelling = aq_base(self.test_parcelling)
        self.assertTrue(hasattr(test_parcelling, 'destination'))

    def test_destination_field_edit(self):
        self.browser.open(self.test_parcelling.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'destination' is not editable"
        self.assertTrue('Destination du lot' in contents, msg)
