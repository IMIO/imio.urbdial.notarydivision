# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.testing import NotaryDivisionFunctionalBrowserTest

from zope.component import getMultiAdapter
from zope.pagetemplate.interfaces import IPageTemplate

import transaction


class TestSingleCheckBoxForDataGridWidgetFunctional(NotaryDivisionFunctionalBrowserTest):
    """
    Test SingleCheckBoxForDataGridWidget which customize the display template to render
    the cadastral reference  (divsion, section, radical, exposant, power) in one colum.
    """

    def setUp(self):
        super(TestSingleCheckBoxForDataGridWidgetFunctional, self).setUp()
        created_estate_value = {
            'locality': '',
            'division': '',
            'section': '',
            'radical': '',
            'bis': '',
            'exposant': '',
            'power': '',
            'surface': '',
            'surface_accuracy': '',
            'built': False,
            'specific_rights': '',
        }
        self.test_divnot.created_estate = [created_estate_value]
        transaction.commit()

    def getBuiltFieldWidget(self, mode):
        view = self.test_divnot.restrictedTraverse('@@{}'.format(mode))
        view.update()
        created_estate_widget = view.widgets['created_estate'].widgets[0]
        built_widget = created_estate_widget.subform.widgets['built']
        return built_widget

    def test_SingleCheckBoxForDataGridWidget_is_widget_of_field_built(self):
        from imio.urbdial.notarydivision.browser.singlecheckbox_for_datagrid import SingleCheckBoxForDataGridWidget
        built_widget = self.getBuiltFieldWidget('view')
        self.assertTrue(isinstance(built_widget, SingleCheckBoxForDataGridWidget))

    def test_custom_display_template_is_registered_for_built_field(self):
        widget = self.getBuiltFieldWidget('view')
        field = widget.field
        template = getMultiAdapter(
            (self.test_divnot, widget.request, widget.form, field, widget),
            IPageTemplate, name='display'
        )
        self.assertTrue(template.filename.endswith('datagrid_checkbox_display.pt'))

    def test_custom_edit_template_is_registered_for_built_field(self):
        widget = self.getBuiltFieldWidget('edit')
        field = widget.field
        template = getMultiAdapter(
            (self.test_divnot, widget.request, widget.form, field, widget),
            IPageTemplate, name='input'
        )
        self.assertTrue(template.filename.endswith('datagrid_checkbox_input.pt'))

    def test_built_field_display_when_set_to_False(self):
        created_estate_value = {
            'locality': '',
            'division': '',
            'section': '',
            'radical': '',
            'bis': '',
            'exposant': '',
            'power': '',
            'surface': '',
            'surface_accuracy': '',
            'built': False,
            'specific_rights': '',
        }
        self.test_divnot.created_estate = [created_estate_value]
        transaction.commit()

        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "Value of field 'built' is not displayed"
        self.assertTrue('<span class="selected-option">Non</span>' in contents, msg)
        self.assertTrue('<span class="selected-option">Oui</span>' not in contents, msg)

    def test_built_field_display_when_set_to_True(self):
        created_estate_value = {
            'locality': '',
            'division': '',
            'section': '',
            'radical': '',
            'bis': '',
            'exposant': '',
            'power': '',
            'surface': '',
            'surface_accuracy': '',
            'built': True,
            'specific_rights': '',
        }
        self.test_divnot.created_estate = [created_estate_value]
        transaction.commit()

        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "Value of field 'built' is not displayed"
        self.assertTrue('<span class="selected-option">Non</span>' not in contents, msg)
        self.assertTrue('<span class="selected-option">Oui</span>' in contents, msg)
