# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.testing import NotaryDivisionFunctionalBrowserTest

import transaction


class TestCreatedParcelListing(NotaryDivisionFunctionalBrowserTest):
    """
    Test CreatedParcel z3c.table listing.
    """

    def _test_createdparcelling_listing_column_display(self, value_name, expected_value, setvalue=None):
        parcel = self.test_parcelling

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
        msg = "created parcel {value_name} '{expected_value}' is not displayed in created parcels listing".format(
            value_name=value_name,
            expected_value=expected_value,
        )
        self.assertTrue(expected_value in contents, msg)

    def test_createdparcelling_number_display(self):
        expected_value = '4242'
        self._test_createdparcelling_listing_column_display('number', expected_value)

    def test_createdparcelling_locality_display(self):
        expected_value = 'Braine-le-Château</td>'

        def set_locality():
            self.test_parcelling.locality = '1440'

        self._test_createdparcelling_listing_column_display('locality', expected_value, set_locality)

    def test_createdparcelling_cadastralref_display(self):
        expected_value = 'A 45 B/2 24 '

        def set_ref():
            self.test_parcelling.division = 'A'
            self.test_parcelling.section = '45'
            self.test_parcelling.radical = 'B'
            self.test_parcelling.bis = '2'
            self.test_parcelling.exposant = '24'

        self._test_createdparcelling_listing_column_display('Cadastral reference', expected_value, set_ref)

    def test_createdparcelling_address_display(self):
        expected_value = '666, saikonji street'

        def set_street():
            self.test_parcelling.street = 'saikonji street'
            self.test_parcelling.street_number = '666'

        self._test_createdparcelling_listing_column_display('street', expected_value, set_street)

    def test_createdparcelling_surface_display(self):
        expected_value = '66ha (mesurée)'

        def set_surface():
            self.test_parcelling.surface = '66ha'
            self.test_parcelling.surface_accuracy = 'mesuree'

        self._test_createdparcelling_listing_column_display('surface', expected_value, set_surface)

    def test_createdparcelling_road_distance_display(self):
        expected_value = '333 m'

        def set_roaddistance():
            self.test_parcelling.road_distance = '333'

        self._test_createdparcelling_listing_column_display('road_distance', expected_value, set_roaddistance)

    def test_createdparcelling_deed_type_display(self):
        expected_value = 'droit de nue propriété</td>'

        def set_deedtype():
            self.test_parcelling.deed_type = 'droit-de-nue-propriete'

        self._test_createdparcelling_listing_column_display('deed_type', expected_value, set_deedtype)

    def test_createdparcelling_other_deedtype_display(self):
        expected_value = 'my yolo deed type</td>'

        def set_deedtype():
            self.test_parcelling.deed_type = 'autre'
            self.test_parcelling.other_deed_type = 'my yolo deed type'

        self._test_createdparcelling_listing_column_display('deed_type', expected_value, set_deedtype)

    def test_createdparcelling_destination_display(self):
        expected_value = 'the wonders of you'
        self._test_createdparcelling_listing_column_display('destination', expected_value)

    def test_createdparcelling_built_display(self):
        expected_value = 'Non</td>'

        def set_built():
            self.test_parcelling.built = False

        self._test_createdparcelling_listing_column_display('built', expected_value, set_built)

    def test_createdparcelling_undivided_display(self):
        expected_value = 'droits des parties</a>'
        self._test_createdparcelling_listing_column_display('undivided_b', expected_value)
