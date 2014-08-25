# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.testing import NotaryDivisionFunctionalBrowserTest

import transaction


class TestInitialParcelListing(NotaryDivisionFunctionalBrowserTest):
    """
    Test InitialParcel z3c.table listing.
    """

    def test_initialparcel_listing_column_display(self, value_name, expected_value, setvalue=None):
        parcel = self.test_initialparcel

        self.browser.open(parcel.absolute_url())
        contents = self.browser.contents
        self.assertTrue(expected_value not in contents)

        if setvalue:
            setvalue()
        else:
            setattr(parcel, value_name, expected_value)
        transaction.commit()

        self.browser.open(parcel.absolute_url())
        contents = self.browser.contents
        msg = "initial parcel {value_name} '{expected_value}' is not displayed in initial parcels listing".format(
            value_name=value_name,
            expected_value=expected_value,
        )
        self.assertTrue(expected_value in contents, msg)

    def test_initialparcel_number_display(self):
        expected_value = '4242'
        self.test_initialparcel_listing_column_display('number', expected_value)

    def test_initialparcel_locality_display(self):
        expected_value = 'Braine-le-Château</td>'

        def setlocality():
            self.test_initialparcel.locality = '1440'

        self.test_initialparcel_listing_column_display('locality', expected_value, setlocality)

    def test_initialparcel_cadastralref_display(self):
        expected_value = 'A 45 B/2 24 '

        def setref():
            self.test_initialparcel.division = 'A'
            self.test_initialparcel.section = '45'
            self.test_initialparcel.radical = 'B'
            self.test_initialparcel.bis = '2'
            self.test_initialparcel.exposant = '24'

        self.test_initialparcel_listing_column_display('Cadastral reference', expected_value, setref)

    def test_initialparcel_surface_display(self):
        expected_value = '66ha'
        self.test_initialparcel_listing_column_display('surface', expected_value)

    def test_initialparcel_actual_use_display(self):
        expected_value = 'the wonders of you'
        self.test_initialparcel_listing_column_display('actual_use', expected_value)

    def test_initialparcel_undivided_display(self):
        expected_value = 'droits des parties</a>'
        self.test_initialparcel_listing_column_display('undivided_a', expected_value)
