# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from Acquisition import aq_base

from plone import api

from imio.urbdial.notarydivision.testing import BrowserTest
from imio.urbdial.notarydivision.testing import EXAMPLE_DIVISION_INTEGRATION
from imio.urbdial.notarydivision.testing import TEST_INSTALL_INTEGRATION

from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD

import unittest


class TestInstall(unittest.TestCase):
    """
    Test installation of imio.urbdial.notarydivision into Plone.
    """

    layer = TEST_INSTALL_INTEGRATION

    def test_portal_type_is_registered(self):
        portal_types = api.portal.get_tool('portal_types')
        registered_types = portal_types.listContentTypes()
        self.assertTrue('NotaryDivision' in registered_types)

    def test_creation_permission_is_cmfAddPortalContent(self):
        portal_types = api.portal.get_tool('portal_types')
        divnot_type = portal_types.NotaryDivision
        self.assertTrue(divnot_type.add_permission == 'cmf.AddPortalContent')


class NotaryDivisionBrowserTest(BrowserTest):
    """
    Helper class factorizing setUp of all NotaryDivision Browser tests.
    """

    layer = EXAMPLE_DIVISION_INTEGRATION

    def setUp(self):
        super(NotaryDivisionBrowserTest, self).setUp()
        self.test_divnot = self.portal.notarydivisions.objectValues()[0]
        self.browserLogin(TEST_USER_NAME, TEST_USER_PASSWORD)


class TestNotaryDivisionFields(NotaryDivisionBrowserTest):
    """
    Test schema fields declaration.
    """

    layer = EXAMPLE_DIVISION_INTEGRATION

    def test_class_registration(self):
        from imio.urbdial.notarydivision.content.NotaryDivision import NotaryDivision
        self.assertTrue(self.test_divnot.__class__ == NotaryDivision)

    def test_schema_registration(self):
        portal_types = api.portal.get_tool('portal_types')
        divnot_type = portal_types.get(self.test_divnot.portal_type)
        self.assertTrue('INotaryDivision' in divnot_type.schema)

    def test_exclude_from_navigation_attribute(self):
        test_divnot = aq_base(self.test_divnot)
        self.assertTrue(hasattr(test_divnot, 'exclude_from_nav'))

    def test_exclude_from_navigation_field_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = 'field exclude_from_nav should be hidden in Display View'
        self.assertTrue('<span id="form-widgets-exclude_from_nav"' not in contents, msg)

    def test_exclude_from_navigation_field_edit(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = 'field exclude_from_nav should be hidden in Display View'
        self.assertTrue('<span class="label">Exclude from navigation</span>' not in contents, msg)

    def test_exclude_from_navigation_field_default_value_is_True(self):
        self.assertTrue(self.test_divnot.exclude_from_nav)

    def test_reference_attribute(self):
        test_divnot = aq_base(self.test_divnot)
        self.assertTrue(hasattr(test_divnot, 'reference'))

    def test_reference_field_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "field 'reference' is not displayed"
        self.assertTrue('id="form-widgets-reference"' in contents, msg)
        msg = "field 'reference' is not translated"
        self.assertTrue('Référence' in contents, msg)

    def test_reference_field_edit(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'reference' is not editable"
        self.assertTrue('Référence' in contents, msg)

    def test_applicants_attribute(self):
        test_divnot = aq_base(self.test_divnot)
        self.assertTrue(hasattr(test_divnot, 'applicants'))

    def test_applicants_field_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "field 'applicants' is not displayed"
        self.assertTrue('form.widgets.applicants' in contents, msg)
        msg = "field 'applicants' is not translated"
        self.assertTrue('Requérant(s)' in contents, msg)

    def test_applicants_field_edit(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'applicants' is not editable"
        self.assertTrue('Requérant(s)' in contents, msg)

    def test_actual_use_attribute(self):
        test_divnot = aq_base(self.test_divnot)
        self.assertTrue(hasattr(test_divnot, 'actual_use'))

    def test_actual_use_field_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "field 'actual_use' is not displayed"
        self.assertTrue('id="form-widgets-actual_use"' in contents, msg)
        msg = "field 'actual_use' is not translated"
        self.assertTrue('Affectation actuelle du bien' in contents, msg)

    def test_actual_use_field_edit(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'actual_use' is not editable"
        self.assertTrue('Affectation actuelle du bien' in contents, msg)


class TestAddNotaryDivision(NotaryDivisionBrowserTest):
    """
    Test NotaryDivision Add form.
    """

    def test_NotaryDivisionAddForm_class_registration(self):
        from imio.urbdial.notarydivision.content.NotaryDivision_view import NotaryDivisionAddForm
        add_form = self.portal.notarydivisions.restrictedTraverse('++add++NotaryDivision')
        self.assertTrue(add_form.form == NotaryDivisionAddForm)


class TestNotaryDivisionEdit(NotaryDivisionBrowserTest):
    """
    Test NotaryDivision Edit form.
    """

    def test_NotaryDivisionEditForm_class_registration(self):
        from imio.urbdial.notarydivision.content.NotaryDivision_view import NotaryDivisionEditForm
        edit = self.test_divnot.restrictedTraverse('@@edit')
        self.assertTrue(isinstance(edit, NotaryDivisionEditForm))


class TestNotaryDivisionView(NotaryDivisionBrowserTest):
    """
    Test NotaryDivision View.
    """

    def test_NotaryDivisionView_class_registration(self):
        from imio.urbdial.notarydivision.content.NotaryDivision_view import NotaryDivisionView
        view = self.test_divnot.restrictedTraverse('view')
        self.assertTrue(isinstance(view, NotaryDivisionView))

    def test_NotaryDivision_excluded_from_navigation(self):
        self.browser.open(self.portal.absolute_url())
        contents = self.browser.contents
        msg = 'test NotaryDivision appears in navigation bar'
        self.assertTrue('<li id="portaltab-test_notarydivision" class="plain">' not in contents, msg)

    def test_view_template_customize_body_slot_of_Plone_main_template(self):
        """
        The 'Last modification' link should not appears.
        """
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = 'Last modification link is still visible.'
        self.assertTrue('<span class="documentAuthor">' not in contents, msg)
        self.assertTrue('<span class="documentModified">' not in contents, msg)
