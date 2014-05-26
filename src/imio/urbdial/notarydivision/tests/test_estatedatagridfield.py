# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.testing import NotaryDivisionBrowserTest
from imio.urbdial.notarydivision.testing import NotaryDivisionFunctionalBrowserTest

from zope.component import getMultiAdapter
from zope.pagetemplate.interfaces import IPageTemplate

import transaction


class TestEstateDataGridField(NotaryDivisionBrowserTest):
    """
    Test EstateDataGridField which customize the display template to render
    the cadastral reference  (divsion, section, radical, exposant, power) in one colum.
    """

    def test_EstateDataGridField_is_widget_of_field_initial_estate(self):
        from imio.urbdial.notarydivision.content.notarydivision_view import EstateDataGridField
        view = self.test_divnot.restrictedTraverse('view')
        view.update()
        initial_estate_widget = view.widgets['initial_estate']
        self.assertTrue(isinstance(initial_estate_widget, EstateDataGridField))

    def test_custom_display_template_is_registered_for_initial_estate_field(self):
        view = self.test_divnot.restrictedTraverse('view')
        view.update()
        field = view.fields['initial_estate']
        widget = view.widgets['initial_estate']
        template = getMultiAdapter(
            (self.test_divnot, view.request, widget.form, field, widget),
            IPageTemplate, name='display'
        )
        self.assertTrue(template.filename.endswith('datagrid_estate_display.pt'))

    def test_custom_display_template_for_initial_estate_field(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        datagrid_columns = ['Commune', 'Référence cadastrale', 'Superficie', 'Droits des parties']
        for label in datagrid_columns:
            msg = "Label '{}' does not appear in 'initial_estate' datagrid header.".format(label)
            self.assertTrue(label in contents, msg)

    def test_EstateDataGridField_is_widget_of_field_created_estate(self):
        from imio.urbdial.notarydivision.content.notarydivision_view import EstateDataGridField
        view = self.test_divnot.restrictedTraverse('view')
        view.update()
        initial_estate_widget = view.widgets['initial_estate']
        self.assertTrue(isinstance(initial_estate_widget, EstateDataGridField))

    def test_custom_display_template_is_registered_for_created_estate_field(self):
        view = self.test_divnot.restrictedTraverse('view')
        view.update()
        field = view.fields['created_estate']
        widget = view.widgets['created_estate']
        template = getMultiAdapter(
            (self.test_divnot, view.request, widget.form, field, widget),
            IPageTemplate, name='display'
        )
        self.assertTrue(template.filename.endswith('datagrid_estate_display.pt'))

    def test_custom_display_template_for_created_estate_field(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        datagrid_columns = [
            'Commune', 'Référence cadastrale', 'Superficie', '(type)',
            'Bâti', 'Droits des parties'
        ]
        for label in datagrid_columns:
            msg = "Label '{}' does not appear in 'created_estate' datagrid header.".format(label)
            self.assertTrue(label in contents, msg)


class TestEstateDataGridFieldFunctional(NotaryDivisionFunctionalBrowserTest):
    """
    Test EstateDataGridField which customize the display template to render
    the cadastral reference  (divsion, section, radical, exposant, power) in one colum.
    """

    def test_encoded_values_of_initial_estate_field_are_displayed(self):
        initial_estate_value = {
            'locality': '5000',
            'division': 'Beez',
            'section': 'A',
            'radical': '42',
            'bis': '^2',
            'exposant': 'E',
            'power': '66',
            'surface': '45 ares',
            'specific_rights': 'Yo moma in pyjama!',
        }
        self.test_divnot.initial_estate = [initial_estate_value]
        transaction.commit()

        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "Locality value of 'initial_estate' field is not displayed"
        self.assertTrue('Namur' in contents, msg)
        msg = "Cadastral reference value of 'initial_estate'field is not correctly displayed"
        self.assertTrue('Beez A 42 ^2 E 66' in contents, msg)
        msg = "Surface value of 'initial_estate' field is not displayed"
        self.assertTrue('45 ares' in contents, msg)
        msg = "Specific rights value of 'initial_estate field' is not displayed"
        self.assertTrue('Yo moma in pyjama!' in contents, msg)

    def test_encoded_values_of_created_estate_field_are_displayed(self):
        created_estate_value = {
            'locality': '5000',
            'division': 'Jambes',
            'section': 'C',
            'radical': '666',
            'bis': '^3',
            'exposant': 'F',
            'power': '9',
            'surface': '314 ares',
            'surface_accuracy': 'measured',
            'built': True,
            'specific_rights': 'We called him tortoise because he taught us.',
        }
        self.test_divnot.created_estate = [created_estate_value]
        transaction.commit()

        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "Locality value of 'created_estate' field is not displayed"
        self.assertTrue('Namur' in contents, msg)
        msg = "Cadastral reference value of 'created_estate'field is not correctly displayed"
        self.assertTrue('Jambes C 666 ^3 F 9' in contents, msg)
        msg = "Surface value of 'created_estate' field is not displayed"
        self.assertTrue('314 ares' in contents, msg)
        msg = "Specific rights value of 'created_estate field' is not displayed"
        self.assertTrue('We called him tortoise because he taught us.' in contents, msg)

    def test_empty_values_display(self):
        created_estate_value = {
            'locality': '',
            'division': None,
            'section': 'A',
            'radical': '42',
            'bis': '^2',
            'exposant': 'E',
            'power': '66',
            'surface': '',
            'surface_accuracy': None,
            'built': None,
            'specific_rights': None,
        }
        self.test_divnot.created_estate = [created_estate_value]
        transaction.commit()

        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "Empty values are not displayed as 'N.C.'"
        self.assertTrue('<span class="discreet">N.C</span>' in contents, msg)
