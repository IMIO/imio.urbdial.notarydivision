# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.testing import EXAMPLE_DIVISION_INTEGRATION

from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import login
from plone.testing.z2 import Browser

import unittest


class TestErgonomy(unittest.TestCase):
    """Test miscellaneous ergonomy changes brought by urbdial"""

    layer = EXAMPLE_DIVISION_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']

        login(self.portal, TEST_USER_NAME)
        self.browser = Browser(self.portal)
        self.browserLogin(TEST_USER_NAME, TEST_USER_PASSWORD)
        self.browser.handleErrors = False

    def browserLogin(self, user, password):
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = password
        self.browser.getControl(name='submit').click()

    def test_plone_searchbox_disabled(self):
        self.browser.open(self.portal.absolute_url())
        contents = self.browser.contents
        msg = 'Plone searchbox is not disabled'
        self.assertTrue('<input id="searchGadget"' not in contents, msg)
        self.assertTrue('<input class="searchButton"' not in contents, msg)

    def test_plone_logo_is_hidden(self):
        self.browser.open(self.portal.absolute_url())
        contents = self.browser.contents
        msg = 'Plone logo is not hidden'
        self.assertTrue('<a id="portal-logo"' not in contents, msg)

    def test_plone_footer_is_hidden(self):
        self.browser.open(self.portal.absolute_url())
        contents = self.browser.contents
        msg = 'Plone footer is not hidden'
        self.assertTrue('<div id="portal-footer">' not in contents, msg)

    def test_plone_site_actions_are_hidden(self):
        self.browser.open(self.portal.absolute_url())
        contents = self.browser.contents
        msg = 'Plone site actions are not hidden'
        self.assertTrue('<li id="siteaction' not in contents, msg)

    def test_plone_portlets_are_hidden(self):
        self.browser.open(self.portal.absolute_url() + '/@@manage-portlets')
        contents = self.browser.contents
        msg = 'Plone site actions are not hidden'
        self.assertTrue('Manage portlets' in contents, msg)
        self.assertTrue('<span class="managedPortletActions">' not in contents, msg)

    def test_site_view_redirects_to_notarydivisions_folder(self):
        self.browser.open(self.portal.absolute_url())
        self.assertTrue(self.browser.url == 'http://nohost/plone/notarydivisions')

    def test_anonymous_is_redirected_to_login_page(self):
        self.browser.open(self.portal.absolute_url() + "/logout")
        self.browser.open(self.portal.absolute_url())
        self.assertTrue(self.browser.url.endswith('/login'))
