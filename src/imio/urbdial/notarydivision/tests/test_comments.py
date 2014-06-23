# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.testing import CommentBrowserTest
from imio.urbdial.notarydivision.testing import CommentFunctionalBrowserTest
from imio.urbdial.notarydivision.testing import TEST_INSTALL_INTEGRATION
from imio.urbdial.notarydivision.testing_vars import TEST_FD_NAME
from imio.urbdial.notarydivision.testing_vars import TEST_FD_PASSWORD
from imio.urbdial.notarydivision.testing_vars import TEST_NOTARY_NAME
from imio.urbdial.notarydivision.testing_vars import TEST_NOTARY_PASSWORD

from plone import api
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

    def test_Observation_is_in_Observation_allowed_content_types(self):
        portal_types = api.portal.get_tool('portal_types')
        observation_type = portal_types.Observation
        self.assertTrue('Observation' in observation_type.allowed_content_types)

    def test_Precision_portal_type_is_registered(self):
        portal_types = api.portal.get_tool('portal_types')
        registered_types = portal_types.listContentTypes()
        self.assertTrue('Precision' in registered_types)

    def test_Precision_creation_permission_is_AddPrecision(self):
        portal_types = api.portal.get_tool('portal_types')
        precision_type = portal_types.Precision
        self.assertTrue(precision_type.add_permission == 'imio.urbdial.notarydivision.AddPrecision')

    def test_PrecisionDemand_portal_type_is_registered(self):
        portal_types = api.portal.get_tool('portal_types')
        registered_types = portal_types.listContentTypes()
        self.assertTrue('PrecisionDemand' in registered_types)

    def test_PrecisionDemand_creation_permission_is_AddObservation(self):
        portal_types = api.portal.get_tool('portal_types')
        precisionDemand_type = portal_types.PrecisionDemand
        self.assertTrue(precisionDemand_type.add_permission == 'imio.urbdial.notarydivision.AddObservation')

    def test_InadmissibleFolder_portal_type_is_registered(self):
        portal_types = api.portal.get_tool('portal_types')
        registered_types = portal_types.listContentTypes()
        self.assertTrue('InadmissibleFolder' in registered_types)

    def test_InadmissibleFolder_creation_permission_is_AddObservation(self):
        portal_types = api.portal.get_tool('portal_types')
        inadmissibleFolder_type = portal_types.InadmissibleFolder
        self.assertTrue(inadmissibleFolder_type.add_permission == 'imio.urbdial.notarydivision.AddObservation')


class TestCommentView(CommentBrowserTest):
    """
    Test comment View.
    """

    def test_CommentView_class_registration(self):
        from imio.urbdial.notarydivision.content.comment_view import CommentView
        view = self.test_observation.restrictedTraverse('view')
        self.assertTrue(isinstance(view, CommentView))

    def test_Observation_view_redirects_to_NotaryDivisionView(self):
        self.browser.open(self.test_observation.absolute_url())
        notary_division_url = self.test_divnot.absolute_url()
        msg = 'Observation view does not redirect to NotaryDivisionView'
        self.assertTrue(self.browser.url == notary_division_url + '/view#comments', msg)

    def test_Comment_addObservation_buttons(self):
        self.browser.open(self.test_observation.absolute_url())
        contents = self.browser.contents
        msg = 'test Comment addObservation button not appears in view'
        self.assertTrue('Add Observation' in contents, msg)

    def test_Comment_addPrecision_buttons(self):
        self.browser.open(self.test_observation.absolute_url())
        contents = self.browser.contents
        msg = 'test Comment AddPrecision button not appears in view'
        self.assertTrue('Add Precision' in contents, msg)

    def test_Comment_addPrecisionDemand_buttons(self):
        self.browser.open(self.test_observation.absolute_url())
        contents = self.browser.contents
        msg = 'test Comment addPrecisionDemand button not appears in view'
        self.assertTrue('Add PrecisionDemand' in contents, msg)

    def test_Comment_addIndmissibleFolder_buttons(self):
        self.browser.open(self.test_observation.absolute_url())
        contents = self.browser.contents
        msg = 'test Comment addInadmissibleFolder button not appears in view'
        self.assertTrue('Add InadmissibleFolder' in contents, msg)


class FunctionalTestCommentView(CommentFunctionalBrowserTest):
    """
    Functional tests on Comment View.
    """

    def test_title_display_on_draft_comment(self):
        self.browser.open(self.test_divnot.absolute_url())

        # In draft, no publication date is displayed.
        contents = self.browser.contents
        self.assertTrue('BROUILLON' in contents)
        self.assertTrue('publié le ' not in contents)

    def test_title_display_on_published_comment(self):
        api.content.transition(self.test_observation, 'Publish')
        api.content.transition(self.test_precision, 'Publish')
        transaction.commit()

        # Once published, title should be updated with publication date.
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = 'Publication date of Observation should de displayed in title'
        self.assertTrue('BROUILLON' not in contents)
        self.assertTrue('publié le ' in contents, msg)

        # Once frozen, title should stay the same.
        api.content.transition(self.test_observation, 'Freeze')
        api.content.transition(self.test_precision, 'Freeze')
        transaction.commit()
        self.assertTrue('BROUILLON' not in contents)
        self.assertTrue('publié le ' in contents, msg)

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

    def test_comments_cannot_be_added_on_frozen_comment(self):
        notarydivision = self.test_divnot

        # freeze comments
        api.content.transition(notarydivision, 'Notify')
        for comment in notarydivision.objectValues():
            api.content.transition(comment, 'Publish')
            api.content.transition(comment, 'Freeze')
        api.content.transition(notarydivision, 'Pass')
        transaction.commit()

        # subcomments cannot be created anymore
        msg = "Creating new comments should not be allowed anymore when notarydivision is in state 'Passed'"
        self.browser_login(TEST_FD_NAME, TEST_FD_PASSWORD)
        self.browser.open(notarydivision.absolute_url())
        contents = self.browser.contents
        self.assertTrue('Add Observation' not in contents, msg)
        self.browser_login(TEST_NOTARY_NAME, TEST_NOTARY_PASSWORD)
        self.browser.open(notarydivision.absolute_url())
        contents = self.browser.contents
        self.assertTrue('Add Precision' not in contents, msg)
