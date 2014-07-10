# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.testing import REAL_INSTALL_INTEGRATION
from imio.urbdial.notarydivision.testing import CommentBrowserTest
from imio.urbdial.notarydivision.testing import WorkflowLocaRolesAssignmentTest
from imio.urbdial.notarydivision.testing_vars import TEST_FD_NAME
from imio.urbdial.notarydivision.testing_vars import TEST_NOTARY_NAME
from imio.urbdial.notarydivision.testing_vars import TEST_TOWNSHIP_NAME

from plone import api

from zope.component import queryMultiAdapter

import unittest


class TestObservationWorkflowDefinition(unittest.TestCase):
    """
    Test Observation workflow.
    """

    layer = REAL_INSTALL_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.wf_tool = api.portal.get_tool('portal_workflow')
        self.observation_wf = self.wf_tool.getWorkflowById('Observation_workflow')

    def test_observation_workflow_is_registered(self):
        available_workflows = self.wf_tool.listWorkflows()
        self.assertTrue('Observation_workflow' in available_workflows)

    def test_observation_workflow_is_bound_to_Observation_type(self):
        Folder_worklows = self.wf_tool.getChainForPortalType('Observation')
        self.assertTrue('Observation_workflow' in Folder_worklows)

    def test_observation_workflow_is_bound_to_InadmissibleFolder_type(self):
        Folder_worklows = self.wf_tool.getChainForPortalType('InadmissibleFolder')
        self.assertTrue('Observation_workflow' in Folder_worklows)

    def test_observation_workflow_is_bound_to_PrecisionDemand_type(self):
        Folder_worklows = self.wf_tool.getChainForPortalType('PrecisionDemand')
        self.assertTrue('Observation_workflow' in Folder_worklows)

    def get_roles_of_permission(self, permission, state='Draft'):
        default_state = self.observation_wf.states[state]
        roles_of_permission = default_state.permission_roles[permission]
        return roles_of_permission

    def test_available_states(self):
        available_states = self.observation_wf.states.keys()

        expected_states = ['Draft', 'Published', 'Frozen']
        for state in expected_states:
            msg = 'state {} is not defined in the Observation workflow'.format(state)
            self.assertTrue(state in available_states, msg)

    def test_permission_mapping_is_the_same_for_each_state(self):
        states = self.observation_wf.states.values()
        default_state = states[0]
        default_permission_roles = default_state.permission_roles

        for state in states:
            msg = 'State {} has different permission mapping than state {}.'.format(
                state.title,
                default_state.title,
            )
            self.assertTrue(state.permission_roles == default_permission_roles, msg)

    def test_available_transitions(self):
        available_transitions = self.observation_wf.transitions.keys()

        expected_transitions = ['Publish', 'Freeze']
        for transition in expected_transitions:
            msg = 'transition {} is not defined in the Observation workflow'.format(transition)
            self.assertTrue(transition in available_transitions, msg)

    def test_Publication_is_restricted_to_ModifyPortalContent_permission(self):
        transition = self.observation_wf.transitions['Publish']
        guard = transition.getGuardSummary()
        self.assertTrue('Modify portal content' in guard)

    def test_Freeze_is_restricted_to_ManagePortal_permission(self):
        transition = self.observation_wf.transitions['Freeze']
        guard = transition.getGuardSummary()
        self.assertTrue('Manage portal' in guard)

    def test_View_permission_roles(self):
        """
        'View' permission should be given to 'Observation Reader', 'Observation
        Manager' and 'Manager' roles.
        """
        roles_of_permission = self.get_roles_of_permission('View')
        self.assertTrue(len(roles_of_permission) == 3)
        self.assertTrue('Observation Manager' in roles_of_permission)
        self.assertTrue('Observation Reader' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_AccessContentsInformation_permission_roles(self):
        """
        'Access contents information' permission should be given to
        'Observation Reader', 'Observation Manager' and 'Manager' roles.
        """
        roles_of_permission = self.get_roles_of_permission('Access contents information')
        self.assertTrue(len(roles_of_permission) == 3)
        self.assertTrue('Observation Manager' in roles_of_permission)
        self.assertTrue('Observation Reader' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_AddPortalContent_permission_roles(self):
        """
        'Add Precision' permission should be given to 'Precision Creator' role.
        """
        roles_of_permission = self.get_roles_of_permission('Add portal content')
        self.assertTrue(len(roles_of_permission) == 3)
        self.assertTrue('Precision Creator' in roles_of_permission)
        self.assertTrue('Observation Creator' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_AddPrecision_permission_roles(self):
        """
        'Add Precision' permission should be given to 'Precision Creator' role.
        """
        roles_of_permission = self.get_roles_of_permission('imio.urbdial.notarydivision: Add Precision')
        self.assertTrue(len(roles_of_permission) == 2)
        self.assertTrue('Precision Creator' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_AddObservation_permission_roles(self):
        """
        'Add Observation' permission should be given to 'Observation Creator' role.
        """
        roles_of_permission = self.get_roles_of_permission('imio.urbdial.notarydivision: Add Observation')
        self.assertTrue(len(roles_of_permission) == 2)
        self.assertTrue('Observation Creator' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_DeleteObjects_permission_roles(self):
        """
        'Delete objects' permission should be given to 'Observation Manager'.
        """
        roles_of_permission = self.get_roles_of_permission('Delete objects')
        self.assertTrue(len(roles_of_permission) == 2)
        self.assertTrue('Observation Manager' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_ModifyPortalContent_permission_roles(self):
        """
        'Modify portal content' permission should be given to 'Observation Manager' role.
        """
        roles_of_permission = self.get_roles_of_permission('Modify portal content')
        self.assertTrue(len(roles_of_permission) == 2)
        self.assertTrue('Observation Manager' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)


class TestObservationWorkflowLocalRolesAssignment(CommentBrowserTest, WorkflowLocaRolesAssignmentTest):
    """
    Test that local roles are assigned to the right groups when creating a
    new observation or when triggering workflow transitions.
    """

    def test_state_role_mapping_registration(self):
        from imio.urbdial.notarydivision.workflows.interfaces import IWorkflowStateRolesMapping
        from imio.urbdial.notarydivision.workflows import observation_workflow

        wf_tool = api.portal.get_tool('portal_workflow')
        observation_wf = wf_tool.getWorkflowById('Observation_workflow')

        mapping = queryMultiAdapter((self.test_observation, observation_wf), IWorkflowStateRolesMapping)
        self.assertTrue(isinstance(mapping, observation_workflow.StateRolesMapping))

    def test_fd_user_roles_on_draft_state(self):
        expected_roles = ('Observation Manager',)
        self._test_roles_of_user_on_stateful_context(
            username=TEST_FD_NAME,
            expected_roles=expected_roles,
            context=self.test_observation,
            state='Draft',
        )

    def test_township_user_roles_on_draft_state(self):
        # no roles expected because it's not the observation's creator
        expected_roles = ()
        self._test_roles_of_user_on_stateful_context(
            username=TEST_TOWNSHIP_NAME,
            expected_roles=expected_roles,
            context=self.test_observation,
            state='Draft',
        )

    def test_notary_user_roles_on_draft_state(self):
        expected_roles = ()
        self._test_roles_of_user_on_stateful_context(
            username=TEST_NOTARY_NAME,
            expected_roles=expected_roles,
            context=self.test_observation,
            state='Draft',
        )

    def test_fd_user_roles_on_published_state(self):
        observation = self.test_observation
        observation.transition('Publish')

        expected_roles = ('Observation Reader',)
        self._test_roles_of_user_on_stateful_context(
            username=TEST_FD_NAME,
            expected_roles=expected_roles,
            context=observation,
            state='Published',
        )

    def test_township_user_roles_on_published_state(self):
        observation = self.test_observation
        observation.transition('Publish')
        # only reader role expected because it's not the observation's creator
        expected_roles = ('Observation Reader',)
        self._test_roles_of_user_on_stateful_context(
            username=TEST_TOWNSHIP_NAME,
            expected_roles=expected_roles,
            context=self.test_observation,
            state='Published',
        )

    def test_notary_user_roles_on_published_state(self):
        observation = self.test_observation
        observation.transition('Publish')

        expected_roles = ('Observation Reader', 'Precision Creator')
        self._test_roles_of_user_on_stateful_context(
            username=TEST_NOTARY_NAME,
            expected_roles=expected_roles,
            context=observation,
            state='Published',
        )

    def test_fd_user_roles_on_frozen_state(self):
        observation = self.test_observation
        observation.transition('Publish')
        observation.transition('Freeze')

        expected_roles = ('Observation Reader',)
        self._test_roles_of_user_on_stateful_context(
            username=TEST_FD_NAME,
            expected_roles=expected_roles,
            context=observation,
            state='Frozen',
        )

    def test_township_user_roles_on_frozen_state(self):
        observation = self.test_observation
        observation.transition('Publish')
        observation.transition('Freeze')

        expected_roles = ('Observation Reader',)
        self._test_roles_of_user_on_stateful_context(
            username=TEST_TOWNSHIP_NAME,
            expected_roles=expected_roles,
            context=observation,
            state='Frozen',
        )

    def test_notary_user_roles_on_frozen_state(self):
        observation = self.test_observation
        observation.transition('Publish')
        observation.transition('Freeze')

        expected_roles = ('Observation Reader',)
        self._test_roles_of_user_on_stateful_context(
            username=TEST_NOTARY_NAME,
            expected_roles=expected_roles,
            context=observation,
            state='Frozen',
        )


class TestPrecisionWorkflowDefinition(unittest.TestCase):
    """
    Test Precision workflow.
    """

    layer = REAL_INSTALL_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.wf_tool = api.portal.get_tool('portal_workflow')
        self.precision_wf = self.wf_tool.getWorkflowById('Precision_workflow')

    def test_precision_workflow_is_registered(self):
        available_workflows = self.wf_tool.listWorkflows()
        self.assertTrue('Precision_workflow' in available_workflows)

    def test_precision_workflow_is_bound_to_Folder_type(self):
        Folder_worklows = self.wf_tool.getChainForPortalType('Precision')
        self.assertTrue('Precision_workflow' in Folder_worklows)

    def get_roles_of_permission(self, permission, state='Draft'):
        default_state = self.precision_wf.states[state]
        roles_of_permission = default_state.permission_roles[permission]
        return roles_of_permission

    def test_available_states(self):
        available_states = self.precision_wf.states.keys()

        expected_states = ['Draft', 'Published', 'Frozen']
        for state in expected_states:
            msg = 'state {} is not defined in the Precision workflow'.format(state)
            self.assertTrue(state in available_states, msg)

    def test_permission_mapping_is_the_same_for_each_state(self):
        states = self.precision_wf.states.values()
        default_state = states[0]
        default_permission_roles = default_state.permission_roles

        for state in states:
            msg = 'State {} has different permission mapping than state {}.'.format(
                state.title,
                default_state.title,
            )
            self.assertTrue(state.permission_roles == default_permission_roles, msg)

    def test_available_transitions(self):
        available_transitions = self.precision_wf.transitions.keys()

        expected_transitions = ['Publish', 'Freeze']
        for transition in expected_transitions:
            msg = 'transition {} is not defined in the Precision workflow'.format(transition)
            self.assertTrue(transition in available_transitions, msg)

    def test_Publication_is_restricted_to_ModifyPortalContent_permission(self):
        transition = self.precision_wf.transitions['Publish']
        guard = transition.getGuardSummary()
        self.assertTrue('Modify portal content' in guard)

    def test_Freeze_is_restricted_to_ManagePortal_permission(self):
        transition = self.precision_wf.transitions['Freeze']
        guard = transition.getGuardSummary()
        self.assertTrue('Manage portal' in guard)

    def test_View_permission_roles(self):
        """
        'View' permission should be given to 'Precision Reader', 'Precision
        Manager' and 'Manager' roles.
        """
        roles_of_permission = self.get_roles_of_permission('View')
        self.assertTrue(len(roles_of_permission) == 3)
        self.assertTrue('Precision Manager' in roles_of_permission)
        self.assertTrue('Precision Reader' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_AccessContentsInformation_permission_roles(self):
        """
        'Access contents information' permission should be given to
        'Precision Reader', 'Precision Manager' and 'Manager' roles.
        """
        roles_of_permission = self.get_roles_of_permission('Access contents information')
        self.assertTrue(len(roles_of_permission) == 3)
        self.assertTrue('Precision Manager' in roles_of_permission)
        self.assertTrue('Precision Reader' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_AddPortalContent_permission_roles(self):
        """
        'Add Precision' permission should be given to 'Precision Creator' role.
        """
        roles_of_permission = self.get_roles_of_permission('Add portal content')
        self.assertTrue(len(roles_of_permission) == 3)
        self.assertTrue('Precision Creator' in roles_of_permission)
        self.assertTrue('Observation Creator' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_AddPrecision_permission_roles(self):
        """
        'Add Precision' permission should be given to 'Precision Creator' role.
        """
        roles_of_permission = self.get_roles_of_permission('imio.urbdial.notarydivision: Add Precision')
        self.assertTrue(len(roles_of_permission) == 2)
        self.assertTrue('Precision Creator' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_AddObservation_permission_roles(self):
        """
        'Add Observation' permission should be given to 'Observation Creator' role.
        """
        roles_of_permission = self.get_roles_of_permission('imio.urbdial.notarydivision: Add Observation')
        self.assertTrue(len(roles_of_permission) == 2)
        self.assertTrue('Observation Creator' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_DeleteObjects_permission_roles(self):
        """
        'Delete objects' permission should be given to 'Precision Manager'.
        """
        roles_of_permission = self.get_roles_of_permission('Delete objects')
        self.assertTrue(len(roles_of_permission) == 2)
        self.assertTrue('Precision Manager' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_ModifyPortalContent_permission_roles(self):
        """
        'Modify portal content' permission should be given to 'Precision Manager' role.
        """
        roles_of_permission = self.get_roles_of_permission('Modify portal content')
        self.assertTrue(len(roles_of_permission) == 2)
        self.assertTrue('Precision Manager' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)


class TestPrecisionWorkflowLocalRolesAssignment(CommentBrowserTest, WorkflowLocaRolesAssignmentTest):
    """
    Test that local roles are assigned to the right groups when creating a
    new precision or when triggering workflow transitions.
    """

    def test_state_role_mapping_registration(self):
        from imio.urbdial.notarydivision.workflows.interfaces import IWorkflowStateRolesMapping
        from imio.urbdial.notarydivision.workflows import precision_workflow

        wf_tool = api.portal.get_tool('portal_workflow')
        precision_wf = wf_tool.getWorkflowById('Precision_workflow')

        mapping = queryMultiAdapter((self.test_precision, precision_wf), IWorkflowStateRolesMapping)
        self.assertTrue(isinstance(mapping, precision_workflow.StateRolesMapping))

    def test_notary_user_roles_on_draft_state(self):
        expected_roles = ('Precision Manager',)
        self._test_roles_of_user_on_stateful_context(
            username=TEST_NOTARY_NAME,
            expected_roles=expected_roles,
            context=self.test_precision,
            state='Draft',
        )

    def test_fd_user_roles_on_draft_state(self):
        expected_roles = ()
        self._test_roles_of_user_on_stateful_context(
            username=TEST_FD_NAME,
            expected_roles=expected_roles,
            context=self.test_precision,
            state='Draft',
        )

    def test_notary_user_roles_on_published_state(self):
        precision = self.test_precision
        precision.transition('Publish')

        expected_roles = ('Precision Reader', 'Precision Creator')
        self._test_roles_of_user_on_stateful_context(
            username=TEST_NOTARY_NAME,
            expected_roles=expected_roles,
            context=precision,
            state='Published',
        )

    def test_fd_user_roles_on_published_state(self):
        precision = self.test_precision
        precision.transition('Publish')

        expected_roles = ('Precision Reader',)
        self._test_roles_of_user_on_stateful_context(
            username=TEST_FD_NAME,
            expected_roles=expected_roles,
            context=precision,
            state='Published',
        )

    def test_fd_user_roles_on_frozen_state(self):
        precision = self.test_precision
        precision.transition('Publish')
        precision.transition('Freeze')

        expected_roles = ('Precision Reader',)
        self._test_roles_of_user_on_stateful_context(
            username=TEST_FD_NAME,
            expected_roles=expected_roles,
            context=precision,
            state='Frozen',
        )

    def test_notary_user_roles_on_frozen_state(self):
        precision = self.test_precision
        precision.transition('Publish')
        precision.transition('Freeze')

        expected_roles = ('Precision Reader',)
        self._test_roles_of_user_on_stateful_context(
            username=TEST_NOTARY_NAME,
            expected_roles=expected_roles,
            context=precision,
            state='Frozen',
        )
