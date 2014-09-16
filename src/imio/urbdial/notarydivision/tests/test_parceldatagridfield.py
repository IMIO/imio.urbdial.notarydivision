# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.testing import NotaryDivisionBrowserTest
from imio.urbdial.notarydivision.testing import NotaryDivisionFunctionalBrowserTest

from zope.component import getMultiAdapter
from zope.pagetemplate.interfaces import IPageTemplate

import transaction


class TestParcelDataGridField(NotaryDivisionBrowserTest):
    """
    Test ParcelDataGridField which customize the display template to render
    the cadastral reference  (divsion, section, radical, exposant, power) in one colum.
    """

    def get_estate_widget_group(self, mode='view'):
        view = self.test_divnot.restrictedTraverse('@@{}'.format(mode))
        view.update()
        estate_fieldset_group = view.groups[1]
        return estate_fieldset_group

    def test_ParcelDataGridField_is_widget_of_field_parcels(self):
        from imio.urbdial.notarydivision.browser.parcel_datagridfield import ParcelDataGridField
        group = self.get_estate_widget_group('view')
        parcel_widget = group.widgets['parcels']
        self.assertTrue(isinstance(parcel_widget, ParcelDataGridField))

    def test_custom_display_template_is_registered_for_parcel_field(self):
        view = self.test_divnot.restrictedTraverse('view')
        group = self.get_estate_widget_group('view')
        field = group.fields['parcels']
        widget = group.widgets['parcels']
        template = getMultiAdapter(
            (self.test_divnot, view.request, widget.form, field, widget),
            IPageTemplate, name='display'
        )
        self.assertTrue(template.filename.endswith('parcel_datagrid_display.pt'))

    def test_custom_display_template_for_parcel_field(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        datagrid_columns = ['Commune', 'Référence cadastrale']
        for label in datagrid_columns:
            msg = "Label '{}' does not appear in 'parcel' datagrid header.".format(label)
            self.assertTrue(label in contents, msg)


class TestParcelDataGridFieldFunctional(NotaryDivisionFunctionalBrowserTest):
    """
    Test ParcelDataGridField which customize the display template to render
    the cadastral reference  (divsion, section, radical, exposant, power) in one colum.
    """

    def test_encoded_values_of_parcel_field_are_displayed(self):
        parcel_value = {
            'locality': '5000',
            'division': 'Beez',
            'section': 'A',
            'radical': '42',
            'bis': '2',
            'exposant': 'E',
            'power': '66',
        }
        self.test_divnot.parcels = [parcel_value]
        transaction.commit()

        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "Locality value of 'parcel' field is not displayed"
        self.assertTrue('Namur' in contents, msg)
        msg = "Cadastral reference value of 'parcel'field is not correctly displayed"
        self.assertTrue('Beez A 42/2 E 66' in contents, msg)
