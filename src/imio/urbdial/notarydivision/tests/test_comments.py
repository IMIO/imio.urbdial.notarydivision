# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.testing import CommentBrowserTest
from imio.urbdial.notarydivision.testing import CommentFunctionalBrowserTest
from imio.urbdial.notarydivision.testing import TEST_INSTALL_INTEGRATION
from imio.urbdial.notarydivision.testing_vars import TEST_FD_NAME
from imio.urbdial.notarydivision.testing_vars import TEST_FD_PASSWORD
from imio.urbdial.notarydivision.testing_vars import TEST_NOTARY_NAME
from imio.urbdial.notarydivision.testing_vars import TEST_NOTARY_PASSWORD
from imio.urbdial.notarydivision.testing_vars import TEST_TOWNSHIP_NAME
from imio.urbdial.notarydivision.testing_vars import TEST_TOWNSHIP_PASSWORD
from imio.urbdial.notarydivision.testing import WorkflowLocaRolesAssignmentTest
from imio.urbdial.notarydivision.utils import translate

from plone import api
from plone.app.testing import login
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
        addObservation = ''.format(
            translate(u'Add'),
            translate(u'Observation').encode('utf-8')
        )
        self.assertTrue(addObservation in contents, msg)

    def test_Comment_addPrecision_buttons(self):
        self.browser.open(self.test_observation.absolute_url())
        contents = self.browser.contents
        msg = 'test Comment AddPrecision button not appears in view'
        addPrecision = ''.format(
            translate(u'Add'),
            translate(u'Precision').encode('utf-8')
        )
        self.assertTrue(addPrecision in contents, msg)

    def test_Comment_addPrecisionDemand_buttons(self):
        self.browser.open(self.test_observation.absolute_url())
        contents = self.browser.contents
        msg = 'test Comment addPrecisionDemand button not appears in view'
        addPrecisionDemand = ''.format(
            translate(u'Add'),
            translate(u'PrecisionDemand').encode('utf-8')
        )
        self.assertTrue(addPrecisionDemand in contents, msg)

    def test_Comment_addIndmissibleFolder_buttons(self):
        self.browser.open(self.test_observation.absolute_url())
        contents = self.browser.contents
        msg = 'test Comment addInadmissibleFolder button not appears in view'
        addInadmissibleFolder = ''.format(
            translate(u'Add'),
            translate(u'InadmissibleFolder').encode('utf-8')
        )
        self.assertTrue(addInadmissibleFolder in contents, msg)


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
        self.test_observation.transition('Publish')
        self.test_precision.transition('Publish')
        transaction.commit()

        # Once published, title should be updated with publication date.
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = 'Publication date of Observation should de displayed in title'
        self.assertTrue('BROUILLON' not in contents)
        self.assertTrue('publié le ' in contents, msg)

        # Once frozen, title should stay the same.
        self.test_observation.transition('Freeze')
        self.test_precision.transition('Freeze')
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

    def test_draft_observation_created_by_dgo4_is_hidden_for_township(self):
        observation_text = "<span>A long time ago in a galaxy far, far away...</span>"
        self.test_observation.text = RichTextValue(observation_text)
        transaction.commit()

        self.browser_login(TEST_TOWNSHIP_NAME, TEST_TOWNSHIP_PASSWORD)
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "Draft Observation created by dgo4 sould not be visible to township"
        self.assertTrue(observation_text not in contents, msg)

    def test_draft_observation_created_by_township_is_hidden_for_dgo4(self):
        notarydivision = self.test_divnot
        self.browser_login(TEST_TOWNSHIP_NAME, TEST_TOWNSHIP_PASSWORD)
        observation = api.content.create(
            type='Observation',
            id='observation_2',
            container=notarydivision,
        )
        observation_text = "<span>A long time ago in a galaxy far, far away...</span>"
        observation.text = RichTextValue(observation_text)
        transaction.commit()

        self.browser_login(TEST_FD_NAME, TEST_FD_PASSWORD)
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "Draft Observation created by township sould not be visible to dgo4"
        self.assertTrue(observation_text not in contents, msg)

    def test_comments_cannot_be_added_on_frozen_comment(self):
        notarydivision = self.test_divnot

        # freeze comments
        for comment in notarydivision.objectValues():
            comment.transition('Publish')
            comment.transition('Freeze')
        notarydivision.transition('Pass')
        transaction.commit()

        # subcomments cannot be created anymore
        msg = "Creating new comments should not be allowed anymore when notarydivision is in state 'Passed'"
        self.browser_login(TEST_FD_NAME, TEST_FD_PASSWORD)
        self.browser.open(notarydivision.absolute_url())
        contents = self.browser.contents
        self.assertTrue('Répondre' not in contents, msg)
        self.browser_login(TEST_NOTARY_NAME, TEST_NOTARY_PASSWORD)
        self.browser.open(notarydivision.absolute_url())
        contents = self.browser.contents
        self.assertTrue('Répondre' not in contents, msg)


class TestObservationCreatorRoleAssignment(CommentBrowserTest, WorkflowLocaRolesAssignmentTest):
    """
    Observation Creator role should be active for dgo4/township only when there's no draft
    dgo4/township observation on the notary division or a comment.
    """

    def test_observation_creator_role_disabled_on_notary_division(self):
        """
        Test Observation Creator role on a notarydivision.
        """
        notarydivision = self.test_divnot

        # When a draft observation exists on the notary division...
        draft_observations = notarydivision.get_comments(portal_type='Observation', state='Draft')
        self.assertTrue(draft_observations)

        # ... FD should not have 'Observation Creator' role on notarydivision.
        expected_roles = ('NotaryDivision Reader',)
        self._test_roles_of_user_on_stateful_context(
            username=TEST_FD_NAME,
            expected_roles=expected_roles,
            context=notarydivision,
            state='In investigation',
        )

    def test_observation_creator_role_disabled_on_precision(self):
        """
        Test Observation Creator disabled role on a notarydivision.
        """
        notarydivision = self.test_divnot
        precision = self.test_precision
        precision.transition('Publish')

        # When a draft observation by FD exists on the notary division...
        draft_observations = notarydivision.get_comments(portal_type='Observation', state='Draft')
        draft_observations = [obs for obs in draft_observations if obs.is_dgo4_or_township() == 'dgo4']
        self.assertTrue(draft_observations)

        # ... FD should not have 'Observation Creator' role on published precision.
        expected_roles = ('Precision Reader',)
        self._test_roles_of_user_on_stateful_context(
            username=TEST_FD_NAME,
            expected_roles=expected_roles,
            context=precision,
            state='Published',
        )

    def test_observation_creator_role_enabled_on_notary_division(self):
        """
        Test Observation Creator role disabled on a precision.
        """
        notarydivision = self.test_divnot

        # When no draft observation by Township agent exists on the notary division...
        draft_observations = notarydivision.get_comments(portal_type='Observation', state='Draft')
        draft_observations = [obs for obs in draft_observations if obs.is_dgo4_or_township() == 'townships']
        self.assertTrue(not draft_observations)

        # ... Township agent should have 'Observation Creator' role on notarydivision.
        expected_roles = ('NotaryDivision Reader', 'Observation Creator')
        self._test_roles_of_user_on_stateful_context(
            username=TEST_TOWNSHIP_NAME,
            expected_roles=expected_roles,
            context=notarydivision,
            state='In investigation',
        )

    def test_observation_creator_role_enabled_on_precision(self):
        """
        Test Observation Creator role enabled on a notarydivision.
        """
        notarydivision = self.test_divnot
        precision = self.test_precision
        precision.transition('Publish')

        # When a draft observation by Township agent exists on the notary division...
        draft_observations = notarydivision.get_comments(portal_type='Observation', state='Draft')
        draft_observations = [obs for obs in draft_observations if obs.is_dgo4_or_township() == 'townships']
        self.assertTrue(not draft_observations)

        # ... Township agent should have 'Observation Creator' role on notarydivision.
        expected_roles = ('Precision Reader', 'Observation Creator')
        self._test_roles_of_user_on_stateful_context(
            username=TEST_TOWNSHIP_NAME,
            expected_roles=expected_roles,
            context=precision,
            state='Published',
        )

    def test_observation_creator_role_restored_on_notary_division(self):
        """
        Test Observation Creator role on a notarydivision.
        """
        notarydivision = self.test_divnot

        # publish the observation as FD user
        login(self.portal, TEST_FD_NAME)
        self.test_observation.transition('Publish')

        # When no draft observation by FD exists on the notary division...
        draft_observations = notarydivision.get_comments(portal_type='Observation', state='Draft')
        draft_observations = [obs for obs in draft_observations if obs.is_dgo4_or_township() == 'dgo4']
        self.assertTrue(not draft_observations)

        # ... FD should have 'Observation Creator' role on notarydivision.
        expected_roles = ('NotaryDivision Reader', 'Observation Creator')
        self._test_roles_of_user_on_stateful_context(
            username=TEST_FD_NAME,
            expected_roles=expected_roles,
            context=notarydivision,
            state='In investigation',
        )

    def test_observation_creator_role_restored_on_precision(self):
        """
        Test Observation Creator restored role on a notarydivision.
        """
        notarydivision = self.test_divnot
        precision = self.test_precision
        precision.transition('Publish')

        # publish the observation as FD user
        login(self.portal, TEST_FD_NAME)
        self.test_observation.transition('Publish')

        # When no draft observation by FD exists on the notary division...
        draft_observations = notarydivision.get_comments(portal_type='Observation', state='Draft')
        draft_observations = [obs for obs in draft_observations if obs.is_dgo4_or_township() == 'dgo4']
        self.assertTrue(not draft_observations)

        # ... FD should have 'Observation Creator' role on published precision.
        expected_roles = ('Precision Reader', 'Observation Creator')
        self._test_roles_of_user_on_stateful_context(
            username=TEST_FD_NAME,
            expected_roles=expected_roles,
            context=precision,
            state='Published',
        )

    def test_observation_creator_role_restored_on_notary_division_on_delete(self):
        """
        Test Observation Creator role on a notarydivision.
        """
        notarydivision = self.test_divnot

        # delete draft observation
        api.content.delete(self.test_observation)

        # When no draft observation by FD exists on the notary division...
        draft_observations = notarydivision.get_comments(portal_type='Observation', state='Draft')
        self.assertTrue(not draft_observations)

        # ... FD should have 'Observation Creator' role on notarydivision.
        expected_roles = ('NotaryDivision Reader', 'Observation Creator')
        self._test_roles_of_user_on_stateful_context(
            username=TEST_FD_NAME,
            expected_roles=expected_roles,
            context=notarydivision,
            state='In investigation',
        )

    def test_observation_creator_role_restored_on_precision_on_delete(self):
        """
        Test Observation Creator restored role on a notarydivision.
        """
        notarydivision = self.test_divnot
        precision = self.test_precision
        precision.transition('Publish')

        # delete draft observation
        api.content.delete(self.test_observation)

        # When no draft observation by FD exists on the notary division...
        draft_observations = notarydivision.get_comments(portal_type='Observation', state='Draft')
        self.assertTrue(not draft_observations)

        # ... FD should have 'Observation Creator' role on published precision.
        expected_roles = ('Precision Reader', 'Observation Creator')
        self._test_roles_of_user_on_stateful_context(
            username=TEST_FD_NAME,
            expected_roles=expected_roles,
            context=precision,
            state='Published',
        )
