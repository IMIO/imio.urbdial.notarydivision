# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.testing import NotaryDivisionFunctionalBrowserTest

import transaction


class TestCreatedParcellingListing(NotaryDivisionFunctionalBrowserTest):
    """
    Test CreatedParcelling z3c.table listing.
    """

    def _test_createdparcelling_listing_column_display(self, value_name, expected_value, setvalue=None):
        parcelling = self.test_parcelling

        self.browser.open(parcelling.absolute_url())
        contents = self.browser.contents
        msg = "created parcelling {value_name} '{expected_value}' is already displayed in created parcellings listing".format(
            value_name=value_name,
            expected_value=expected_value,
        )
        self.assertTrue(expected_value not in contents, msg)

        if setvalue:
            setvalue()
        else:
            setattr(parcelling, value_name, expected_value)
        transaction.commit()

        self.browser.open(parcelling.absolute_url())
        contents = self.browser.contents
        msg = "created parcelling {value_name} '{expected_value}' is not displayed in created parcellings listing".format(
            value_name=value_name,
            expected_value=expected_value,
        )
        self.assertTrue(expected_value in contents, msg)

    def test_createdparcelling_number_display(self):
        expected_value = '4242'
        self._test_createdparcelling_listing_column_display('number', expected_value)

    def test_createdparcelling_localistation_display(self):
        expected_value = 'hawaii'
        self._test_createdparcelling_listing_column_display('localisation', expected_value)

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

    def test_createdparcelling_destination_display(self):
        expected_value = 'the wonders of you'
        self._test_createdparcelling_listing_column_display('destination', expected_value)

    def test_createdparcelling_ceded_parcelling_display(self):
        # set undivided to true so there no 'Non' displayed on the view
        self.test_divnot.undivided = True
        transaction.commit()
        expected_value = 'Non</td>'

        def set_ceded_parcelling():
            self.test_parcelling.ceded_parcelling = False

        self._test_createdparcelling_listing_column_display('ceded_parcelling', expected_value, set_ceded_parcelling)

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

    def test_createdparcelling_built_display(self):
        # set undivided to true so there no 'Non' displayed on the view
        self.test_divnot.undivided = True
        transaction.commit()
        expected_value = 'Non</td>'

        def set_built():
            self.test_parcelling.built = False

        self._test_createdparcelling_listing_column_display('built', expected_value, set_built)

    def test_createdparcelling_undivided_display(self):
        expected_value = 'droits des parties</a>'

        def set_undivided():
            self.test_parcelling.undivided = True

        self._test_createdparcelling_listing_column_display('undivided', expected_value, set_undivided)
