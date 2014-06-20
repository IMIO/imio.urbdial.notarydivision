# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.testing import REAL_INSTALL_INTEGRATION
from imio.urbdial.notarydivision.testing import CommentBrowserTest

from plone import api

from zope.component import queryAdapter

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

    def test_observation_workflow_is_bound_to_Folder_type(self):
        Folder_worklows = self.wf_tool.getChainForPortalType('Observation')
        self.assertTrue('Observation_workflow' in Folder_worklows)

    def get_roles_of_permission(self, permission, state='Draft'):
        default_state = self.observation_wf.states[state]
        roles_of_permission = default_state.permission_roles[permission]
        return roles_of_permission

    def test_available_states(self):
        available_states = self.observation_wf.states.keys()

        expected_states = ['Draft', 'Published']
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

        expected_transitions = ['Publish']
        for transition in expected_transitions:
            msg = 'transition {} is not defined in the Observation workflow'.format(transition)
            self.assertTrue(transition in available_transitions, msg)

    def test_Publication_is_restricted_to_ModifyPortalContent_permission(self):
        transition = self.observation_wf.transitions['Publish']
        guard = transition.getGuardSummary()
        self.assertTrue('Modify portal content' in guard)

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
        'Add Observation' permission should be given to 'Observation Creator' role.
        """
        roles_of_permission = self.get_roles_of_permission('imio.urbdial.notarydivision: Add Observation')
        self.assertTrue(len(roles_of_permission) == 2)
        self.assertTrue('Observation Creator' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_DeleteObjects_permission_roles(self):
        """
        'Delete Objects' permission should be given to 'Observation Manager'.
        """
        roles_of_permission = self.get_roles_of_permission('Delete Objects')
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

    def test_observation_workflow_provides_IObservationWorkflow(self):
        from imio.urbdial.notarydivision.workflows.interfaces import IObservationWorkflow

        wf_tool = api.portal.get_tool('portal_workflow')
        observation_wf = wf_tool.getWorkflowById('Observation_workflow')

        self.assertTrue(IObservationWorkflow.providedBy(observation_wf))

    def test_state_role_mapping_registration(self):
        from imio.urbdial.notarydivision.workflows.interfaces import IWorkflowStateRolesMapping
        from imio.urbdial.notarydivision.workflows import observation_workflow

        wf_tool = api.portal.get_tool('portal_workflow')
        observation_wf = wf_tool.getWorkflowById('Observation_workflow')

        mapping = queryAdapter(observation_wf, IWorkflowStateRolesMapping)
        self.assertTrue(isinstance(mapping, observation_workflow.StateRolesMapping))


class TestObservationWorkflowLocalRolesAssignment(CommentBrowserTest):
    """
    Test that local roles are assigned to the right groups when creating a
    new observation or when triggering workflow transitions.
    """

    def test_dgo4_group_has_ObservationManager_role_on_draft_state(self):
        observation = self.test_observation
        state = 'Draft'
        group = 'dgo4'
        expected_role = 'Observation Manager'
        self.assertTrue(api.content.get_state(observation) == state)
        local_roles_of_dgo4 = observation.get_local_roles_for_userid(group)
        msg = "Group '{}' should have the the local role '{}' on Observation with state '{}'".format(
            group,
            expected_role,
            state
        )
        self.assertTrue(expected_role in local_roles_of_dgo4, msg)

    def test_dgo4_group_has_ObservationCreator_role_on_published_state(self):
        observation = self.test_observation
        state = 'Published'
        group = 'dgo4'
        expected_role = 'Observation Creator'
        api.content.transition(observation, 'Publish')
        self.assertTrue(api.content.get_state(observation) == state)
        local_roles_of_dgo4 = observation.get_local_roles_for_userid(group)
        msg = "Group '{}' should have the the local role '{}' on Observation with state '{}'".format(
            group,
            expected_role,
            state
        )
        self.assertTrue(expected_role in local_roles_of_dgo4, msg)

    def test_dgo4_group_has_ObservationReader_role_on_published_state(self):
        observation = self.test_observation
        state = 'Published'
        group = 'dgo4'
        expected_role = 'Observation Reader'
        api.content.transition(observation, 'Publish')
        self.assertTrue(api.content.get_state(observation) == state)
        local_roles_of_dgo4 = observation.get_local_roles_for_userid(group)
        msg = "Group '{}' should have the the local role '{}' on Observation with state '{}'".format(
            group,
            expected_role,
            state
        )
        self.assertTrue(expected_role in local_roles_of_dgo4, msg)

    def test_notaries_group_has_ObservationReader_role_on_published_state(self):
        observation = self.test_observation
        state = 'Published'
        group = 'notaries'
        expected_role = 'Observation Reader'
        api.content.transition(observation, 'Publish')
        self.assertTrue(api.content.get_state(observation) == state)
        local_roles_of_notaries = observation.get_local_roles_for_userid(group)
        msg = "Group '{}' should have the the local role '{}' on Observation with state '{}'".format(
            group,
            expected_role,
            state
        )
        self.assertTrue(expected_role in local_roles_of_notaries, msg)
