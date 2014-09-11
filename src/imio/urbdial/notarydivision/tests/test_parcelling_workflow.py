# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.testing import REAL_INSTALL_INTEGRATION
from imio.urbdial.notarydivision.testing import NotaryDivisionBrowserTest
from imio.urbdial.notarydivision.testing import WorkflowLocaRolesAssignmentTest
from imio.urbdial.notarydivision.testing_vars import TEST_FD_NAME
from imio.urbdial.notarydivision.testing_vars import TEST_NOTARY_NAME
from imio.urbdial.notarydivision.testing_vars import TEST_TOWNSHIP_NAME

from plone import api

from zope.component import queryMultiAdapter

import unittest


class TestParcellingWorkflowDefinition(unittest.TestCase):
    """
    Test Parcelling workflow.
    """

    layer = REAL_INSTALL_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.wf_tool = api.portal.get_tool('portal_workflow')
        self.parcelling_wf = self.wf_tool.getWorkflowById('Parcelling_workflow')

    def test_parcelling_workflow_is_registered(self):
        available_workflows = self.wf_tool.listWorkflows()
        self.assertTrue('Parcelling_workflow' in available_workflows)

    def test_parcelling_workflow_is_bound_to_CreatedParcelling_type(self):
        Folder_worklows = self.wf_tool.getChainForPortalType('CreatedParcelling')
        self.assertTrue('Parcelling_workflow' in Folder_worklows)

    def get_roles_of_permission(self, permission, state='Draft'):
        default_state = self.parcelling_wf.states[state]
        roles_of_permission = default_state.permission_roles[permission]
        return roles_of_permission

    def test_available_states(self):
        available_states = self.parcelling_wf.states.keys()

        expected_states = ['Draft', 'Published']
        for state in expected_states:
            msg = 'state {} is not defined in the Parcelling workflow'.format(state)
            self.assertTrue(state in available_states, msg)

        for state in available_states:
            msg = 'state {} is defined in the Parcelling workflow but was not expected'.format(state)
            self.assertTrue(state in expected_states, msg)

    def test_permission_mapping_is_the_same_for_each_state(self):
        states = self.parcelling_wf.states.values()
        default_state = states[0]
        default_permission_roles = default_state.permission_roles

        for state in states:
            msg = 'State {} has different permission mapping than state {}.'.format(
                state.title,
                default_state.title,
            )
            self.assertTrue(state.permission_roles == default_permission_roles, msg)

    def test_available_transitions(self):
        available_transitions = self.parcelling_wf.transitions.keys()

        expected_transitions = ['Publish']
        for transition in expected_transitions:
            msg = 'transition {} is not defined in the Parcelling workflow'.format(transition)
            self.assertTrue(transition in available_transitions, msg)

        for transition in available_transitions:
            msg = 'transition {} is defined in the Parcelling workflow but was not expected'.format(transition)
            self.assertTrue(transition in expected_transitions, msg)

    def test_Publish_is_restricted_to_ManagePortal_permission(self):
        transition = self.parcelling_wf.transitions['Publish']
        guard = transition.getGuardSummary()
        self.assertTrue('Manage portal' in guard)

    def test_View_permission_roles(self):
        """
        'View' permission should be given to 'Parcelling reader', 'Parcelling Manager'
        and 'Manager' roles.
        """
        roles_of_permission = self.get_roles_of_permission('View')
        self.assertTrue(len(roles_of_permission) == 3)
        self.assertTrue('Parcelling Manager' in roles_of_permission)
        self.assertTrue('Parcelling Reader' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_AccessContentsInformation_permission_roles(self):
        """
        'Access contents information' permission should be given to
        'Parcelling reader', 'Parcelling Manager' and 'Manager' roles.
        """
        roles_of_permission = self.get_roles_of_permission('Access contents information')
        self.assertTrue(len(roles_of_permission) == 3)
        self.assertTrue('Parcelling Manager' in roles_of_permission)
        self.assertTrue('Parcelling Reader' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_DeleteObjects_permission_roles(self):
        """
        'Delete objects' permission should be given to 'Parcelling Manager'.
        """
        roles_of_permission = self.get_roles_of_permission('Delete objects')
        self.assertTrue(len(roles_of_permission) == 2)
        self.assertTrue('Parcelling Manager' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_ModifyPortalContent_permission_roles(self):
        """
        'Modify portal content' permission should be given to 'Parcelling Manager' role.
        """
        roles_of_permission = self.get_roles_of_permission('Modify portal content')
        self.assertTrue(len(roles_of_permission) == 2)
        self.assertTrue('Parcelling Manager' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)


class TestParcellingWorkflowLocalRolesAssignment(NotaryDivisionBrowserTest, WorkflowLocaRolesAssignmentTest):
    """
    Test that local roles are assigned to the right groups when creating a
    new parcelling or when triggering workflow transitions.
    """

    def test_state_role_mapping_registration(self):
        from imio.urbdial.notarydivision.workflows.interfaces import IWorkflowStateRolesMapping
        from imio.urbdial.notarydivision.workflows import parcelling_workflow

        wf_tool = api.portal.get_tool('portal_workflow')
        parcelling_wf = wf_tool.getWorkflowById('Parcelling_workflow')

        mapping = queryMultiAdapter((self.test_parcelling, parcelling_wf), IWorkflowStateRolesMapping)
        self.assertTrue(isinstance(mapping, parcelling_workflow.StateRolesMapping))

    def test_notary_user_roles_on_draft_state(self):
        expected_roles = ('Parcelling Manager',)
        self._test_roles_of_user_on_stateful_context(
            username=TEST_NOTARY_NAME,
            expected_roles=expected_roles,
            context=self.test_parcelling,
            state='Draft',
        )

    def test_fd_user_roles_on_draft_state(self):
        expected_roles = ()
        self._test_roles_of_user_on_stateful_context(
            username=TEST_FD_NAME,
            expected_roles=expected_roles,
            context=self.test_parcelling,
            state='Draft',
        )

    def test_township_user_roles_on_draft_state(self):
        expected_roles = ()
        self._test_roles_of_user_on_stateful_context(
            username=TEST_TOWNSHIP_NAME,
            expected_roles=expected_roles,
            context=self.test_parcelling,
            state='Draft',
        )

    def test_notary_user_roles_on_published_state(self):
        parcelling = self.test_parcelling
        parcelling.transition('Publish')

        expected_roles = ('Parcelling Reader',)
        self._test_roles_of_user_on_stateful_context(
            username=TEST_NOTARY_NAME,
            expected_roles=expected_roles,
            context=parcelling,
            state='Published',
        )

    def test_fd_user_roles_on_published_state(self):
        parcelling = self.test_parcelling
        parcelling.transition('Publish')

        expected_roles = ('Parcelling Reader',)
        self._test_roles_of_user_on_stateful_context(
            username=TEST_FD_NAME,
            expected_roles=expected_roles,
            context=parcelling,
            state='Published',
        )

    def test_township_user_roles_on_published_state(self):
        parcelling = self.test_parcelling
        parcelling.transition('Publish')

        expected_roles = ('Parcelling Reader',)
        self._test_roles_of_user_on_stateful_context(
            username=TEST_TOWNSHIP_NAME,
            expected_roles=expected_roles,
            context=parcelling,
            state='Published',
        )
