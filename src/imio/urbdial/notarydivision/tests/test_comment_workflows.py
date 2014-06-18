# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.testing import REAL_INSTALL_INTEGRATION

from plone import api

import unittest


class TestObservationWorkflow(unittest.TestCase):
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

    def test_states(self):
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

    def test_View_permission_roles(self):
        """
        'View' permission should be given to 'Observation Reader' and 'Manager' roles.
        """
        roles_of_permission = self.get_roles_of_permission('View')
        self.assertTrue(len(roles_of_permission) == 2)
        self.assertTrue('Observation Reader' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_AccessContentsInformation_permission_roles(self):
        """
        'Access contents information' permission should be given to
        'Observation Reader' and 'Manager' roles.
        """
        roles_of_permission = self.get_roles_of_permission('Access contents information')
        self.assertTrue(len(roles_of_permission) == 2)
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
