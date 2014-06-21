# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.testing import REAL_INSTALL_INTEGRATION
from imio.urbdial.notarydivision.testing import WorkflowLocaRolesAssignmentTest
from imio.urbdial.notarydivision.testing_vars import TEST_FD_NAME
from imio.urbdial.notarydivision.testing_vars import TEST_NOTARY_NAME

from plone import api

from zope.component import queryAdapter

import unittest


class TestNotificationWorkflowDefinition(unittest.TestCase):
    """
    Test Notification workflow.
    """

    layer = REAL_INSTALL_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.wf_tool = api.portal.get_tool('portal_workflow')
        self.notification_wf = self.wf_tool.getWorkflowById('Notification_workflow')

    def test_notification_workflow_is_registered(self):
        available_workflows = self.wf_tool.listWorkflows()
        self.assertTrue('Notification_workflow' in available_workflows)

    def test_notification_workflow_is_bound_to_Folder_type(self):
        Folder_worklows = self.wf_tool.getChainForPortalType('NotaryDivision')
        self.assertTrue('Notification_workflow' in Folder_worklows)

    def get_roles_of_permission(self, permission, state='In preparation'):
        default_state = self.notification_wf.states[state]
        roles_of_permission = default_state.permission_roles[permission]
        return roles_of_permission

    def test_available_states(self):
        available_states = self.notification_wf.states.keys()

        expected_states = ['In preparation', 'In investigation', 'Passed', 'Cancelled']
        for state in expected_states:
            msg = 'state {} is not defined in the Notification workflow'.format(state)
            self.assertTrue(state in available_states, msg)

        for state in available_states:
            msg = 'state {} is defined in the Notification workflow but was not expected'.format(state)
            self.assertTrue(state in expected_states, msg)

    def test_permission_mapping_is_the_same_for_each_state(self):
        states = self.notification_wf.states.values()
        default_state = states[0]
        default_permission_roles = default_state.permission_roles

        for state in states:
            msg = 'State {} has different permission mapping than state {}.'.format(
                state.title,
                default_state.title,
            )
            self.assertTrue(state.permission_roles == default_permission_roles, msg)

    def test_available_transitions(self):
        available_transitions = self.notification_wf.transitions.keys()

        expected_transitions = ['Notify', 'Cancel', 'Pass', 'Restart']
        for transition in expected_transitions:
            msg = 'transition {} is not defined in the Notification workflow'.format(transition)
            self.assertTrue(transition in available_transitions, msg)

        for transition in available_transitions:
            msg = 'transition {} is defined in the Notification workflow but was not expected'.format(transition)
            self.assertTrue(transition in expected_transitions, msg)

    def test_Notify_is_restricted_to_ModifyPortalContent_permission(self):
        transition = self.notification_wf.transitions['Notify']
        guard = transition.getGuardSummary()
        self.assertTrue('imio.urbdial.notarydivision: Manage notification' in guard)

    def test_Pass_is_restricted_to_ModifyPortalContent_permission(self):
        transition = self.notification_wf.transitions['Pass']
        guard = transition.getGuardSummary()
        self.assertTrue('imio.urbdial.notarydivision: Manage notification' in guard)

    def test_Cancel_is_restricted_to_ModifyPortalContent_permission(self):
        transition = self.notification_wf.transitions['Cancel']
        guard = transition.getGuardSummary()
        self.assertTrue('imio.urbdial.notarydivision: Manage notification' in guard)

    def test_Restart_is_restricted_to_ModifyPortalContent_permission(self):
        transition = self.notification_wf.transitions['Restart']
        guard = transition.getGuardSummary()
        self.assertTrue('Manage portal' in guard)

    def test_View_permission_roles(self):
        """
        'View' permission should be given to 'NotaryDivision Reader', 'NotaryDivision
        Manager' and 'Manager' roles.
        """
        roles_of_permission = self.get_roles_of_permission('View')
        self.assertTrue(len(roles_of_permission) == 3)
        self.assertTrue('NotaryDivision Manager' in roles_of_permission)
        self.assertTrue('NotaryDivision Reader' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_AccessContentsInformation_permission_roles(self):
        """
        'Access contents information' permission should be given to
        'NotaryDivision Reader', 'NotaryDivision Manager' and 'Manager' roles.
        """
        roles_of_permission = self.get_roles_of_permission('Access contents information')
        self.assertTrue(len(roles_of_permission) == 3)
        self.assertTrue('NotaryDivision Manager' in roles_of_permission)
        self.assertTrue('NotaryDivision Reader' in roles_of_permission)
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
        'Delete Objects' permission should be given to 'NotaryDivision Manager'.
        """
        roles_of_permission = self.get_roles_of_permission('Delete Objects')
        self.assertTrue(len(roles_of_permission) == 2)
        self.assertTrue('NotaryDivision Manager' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_ModifyPortalContent_permission_roles(self):
        """
        'Modify portal content' permission should be given to 'NotaryDivision Manager' role.
        """
        roles_of_permission = self.get_roles_of_permission('Modify portal content')
        self.assertTrue(len(roles_of_permission) == 2)
        self.assertTrue('NotaryDivision Manager' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_notification_workflow_provides_INotificationWorkflow(self):
        from imio.urbdial.notarydivision.workflows.interfaces import INotificationWorkflow

        wf_tool = api.portal.get_tool('portal_workflow')
        notification_wf = wf_tool.getWorkflowById('Notification_workflow')

        self.assertTrue(INotificationWorkflow.providedBy(notification_wf))

    def test_state_role_mapping_registration(self):
        from imio.urbdial.notarydivision.workflows.interfaces import IWorkflowStateRolesMapping
        from imio.urbdial.notarydivision.workflows import notification_workflow

        wf_tool = api.portal.get_tool('portal_workflow')
        notification_wf = wf_tool.getWorkflowById('Notification_workflow')

        mapping = queryAdapter(notification_wf, IWorkflowStateRolesMapping)
        self.assertTrue(isinstance(mapping, notification_workflow.StateRolesMapping))


class TestNotificationWorkflowLocalRolesAssignment(WorkflowLocaRolesAssignmentTest):
    """
    Test that local roles are assigned to the right groups when creating a
    new notarydivision or when triggering workflow transitions.
    """

    def test_notary_user_roles_on_preparation_state(self):
        expected_roles = ('NotaryDivision Manager', 'Notification Manager')
        self._test_roles_of_user_on_stateful_context(
            username=TEST_NOTARY_NAME,
            expected_roles=expected_roles,
            context=self.test_divnot,
            state='In preparation',
        )

    def test_fd_user_roles_on_preparation_state(self):
        expected_roles = ()
        self._test_roles_of_user_on_stateful_context(
            username=TEST_FD_NAME,
            expected_roles=expected_roles,
            context=self.test_divnot,
            state='In preparation',
        )

    def test_notary_user_roles_on_investigation_state(self):
        notarydivision = self.test_divnot
        api.content.transition(notarydivision, 'Notify')

        expected_roles = ('NotaryDivision Reader', 'Notification Manager', 'Precision Creator')
        self._test_roles_of_user_on_stateful_context(
            username=TEST_NOTARY_NAME,
            expected_roles=expected_roles,
            context=notarydivision,
            state='In investigation',
        )

    def test_fd_user_roles_on_investigation_state(self):
        notarydivision = self.test_divnot
        api.content.transition(notarydivision, 'Notify')

        expected_roles = ('NotaryDivision Reader', 'Observation Creator')
        self._test_roles_of_user_on_stateful_context(
            username=TEST_FD_NAME,
            expected_roles=expected_roles,
            context=notarydivision,
            state='In investigation',
        )

    def test_notary_user_roles_on_passed_state(self):
        notarydivision = self.test_divnot
        api.content.transition(notarydivision, 'Notify')
        api.content.transition(notarydivision, 'Pass')

        expected_roles = ('NotaryDivision Reader',)
        self._test_roles_of_user_on_stateful_context(
            username=TEST_NOTARY_NAME,
            expected_roles=expected_roles,
            context=notarydivision,
            state='Passed',
        )

    def test_fd_user_roles_on_passed_state(self):
        notarydivision = self.test_divnot
        api.content.transition(notarydivision, 'Notify')
        api.content.transition(notarydivision, 'Pass')

        expected_roles = ('NotaryDivision Reader',)
        self._test_roles_of_user_on_stateful_context(
            username=TEST_FD_NAME,
            expected_roles=expected_roles,
            context=notarydivision,
            state='Passed',
        )

    def test_notary_user_roles_on_cancelled_state(self):
        notarydivision = self.test_divnot
        api.content.transition(notarydivision, 'Notify')
        api.content.transition(notarydivision, 'Cancel')

        expected_roles = ('NotaryDivision Reader',)
        self._test_roles_of_user_on_stateful_context(
            username=TEST_NOTARY_NAME,
            expected_roles=expected_roles,
            context=notarydivision,
            state='Cancelled',
        )

    def test_fd_user_roles_on_cancelled_state(self):
        notarydivision = self.test_divnot
        api.content.transition(notarydivision, 'Notify')
        api.content.transition(notarydivision, 'Cancel')

        expected_roles = ('NotaryDivision Reader',)
        self._test_roles_of_user_on_stateful_context(
            username=TEST_FD_NAME,
            expected_roles=expected_roles,
            context=notarydivision,
            state='Cancelled',
        )
