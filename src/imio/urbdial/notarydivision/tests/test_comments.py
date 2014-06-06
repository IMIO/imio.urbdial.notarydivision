# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.testing import CommentBrowserTest
from imio.urbdial.notarydivision.testing import CommentFunctionalBrowserTest
from imio.urbdial.notarydivision.testing import TEST_INSTALL_INTEGRATION
from imio.urbdial.notarydivision.testing_vars import TEST_FD_NAME
from imio.urbdial.notarydivision.testing_vars import TEST_FD_ID
from imio.urbdial.notarydivision.testing_vars import TEST_FD_PASSWORD

from plone import api
from plone.app.testing import setRoles
from plone.app.textfield.value import RichTextValue

import transaction

import unittest


class TestInstall(unittest.TestCase):
    """
    Test portal_types install.
    """

    layer = TEST_INSTALL_INTEGRATION

    def test_Observation_portal_type_is_registered(self):
        portal_types = api.portal.get_tool('portal_types')
        registered_types = portal_types.listContentTypes()
        self.assertTrue('Observation' in registered_types)

    def test_Observation_creation_permission_is_AddObservation(self):
        portal_types = api.portal.get_tool('portal_types')
        observation_type = portal_types.Observation
        self.assertTrue(observation_type.add_permission == 'imio.urbdial.notarydivision.AddObservation')

    def test_Precision_creation_permission_is_AddPrecision(self):
        portal_types = api.portal.get_tool('portal_types')
        precision_type = portal_types.Precision
        self.assertTrue(precision_type.add_permission == 'imio.urbdial.notarydivision.AddPrecision')

    def test_Observation_is_in_Observation_allowed_content_types(self):
        portal_types = api.portal.get_tool('portal_types')
        observation_type = portal_types.Observation
        self.assertTrue('Observation' in observation_type.allowed_content_types)

    def test_Precision_portal_type_is_registered(self):
        portal_types = api.portal.get_tool('portal_types')
        registered_types = portal_types.listContentTypes()
        self.assertTrue('Precision' in registered_types)


class TestCommentView(CommentBrowserTest):
    """
    Test comment View.
    """

    def test_CommentView_class_registration(self):
        from imio.urbdial.notarydivision.content.comment_view import CommentView
        view = self.test_observation.restrictedTraverse('comment_view')
        self.assertTrue(isinstance(view, CommentView))

    def test_Observation_view_redirects_to_NotaryDivisionView(self):
        self.browser.open(self.test_observation.absolute_url())
        notary_division_url = self.test_divnot.absolute_url()
        msg = 'Observation view does not redirect to NotaryDivisionView'
        self.assertTrue(self.browser.url == notary_division_url + '/view#observations', msg)


class FunctionalTestCommentView(CommentFunctionalBrowserTest):
    """
    Functional tests on Comment View.
    """

    def test_Observation_text_display(self):
        observation_text = "<span>A long time ago in a galaxy far, far away...</span>"

        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        self.assertTrue(observation_text not in contents)

        self.test_observation.text = RichTextValue(observation_text)
        transaction.commit()
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        self.assertTrue(observation_text in contents)

    def test_show_Observation_only_if_user_has_View_permission(self):

        self.browser_login(TEST_FD_NAME, TEST_FD_PASSWORD)
        observation_text = "<span>A long time ago in a galaxy far, far away...</span>"
        self.test_observation.text = RichTextValue(observation_text)
        transaction.commit()

        # Observation should not be visible yet.
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        self.assertTrue(observation_text not in contents)

        # Set Observation Reader role to our user.
        setRoles(self.portal, TEST_FD_ID, ['Observation Reader'])
        transaction.commit()

        # The observation should now be visible.
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        self.assertTrue(observation_text in contents)
