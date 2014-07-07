# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.testing import REAL_INSTALL_INTEGRATION

from plone import api

import unittest


class TestConfigFolderWorkflow(unittest.TestCase):
    """
    Test Config folder workflow.
    """

    layer = REAL_INSTALL_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.wf_tool = api.portal.get_tool('portal_workflow')

    def test_config_folder_workflow_is_registered(self):
        available_workflows = self.wf_tool.listWorkflows()
        self.assertTrue('Config_folder_workflow' in available_workflows)

    def test_config_folder_workflow_is_bound_to_Folder_type(self):
        Folder_worklows = self.wf_tool.getChainForPortalType('ConfigFolder')
        self.assertTrue('Config_folder_workflow' in Folder_worklows)

    def get_roles_of_permission(self, permission):
        config_folder_wf = self.wf_tool.getWorkflowById('Config_folder_workflow')
        default_state = config_folder_wf.states['Default']
        roles_of_permission = default_state.permission_roles[permission]
        return roles_of_permission

    def test_View_permission_roles(self):
        """
        View should be given to 'Config Manager' and 'Manager' roles.
        """
        roles_of_permission = self.get_roles_of_permission('View')
        self.assertTrue(len(roles_of_permission) == 2)
        self.assertTrue('Config Manager' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_AccessContentsInformation_permission_roles(self):
        """
        'Access contents information' permission should be given to
        'Config Manager' and 'Manager' roles.
        """
        roles_of_permission = self.get_roles_of_permission('Access contents information')
        self.assertTrue(len(roles_of_permission) == 2)
        self.assertTrue('Config Manager' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_AddPortalContent_permission_roles(self):
        """
        'Add portal content' permission should be given to 'Config Manager' roles.
        """
        roles_of_permission = self.get_roles_of_permission('Add portal content')
        self.assertTrue(len(roles_of_permission) == 2)
        self.assertTrue('Config Manager' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_DeleteObjects_permission_roles(self):
        """
        'Delete objects' permission should be given to 'Config Manager' and
        'Manager roles.
        """
        roles_of_permission = self.get_roles_of_permission('Delete objects')
        self.assertTrue(len(roles_of_permission) == 2)
        self.assertTrue('Config Manager' in roles_of_permission)
        self.assertTrue('Manager' in roles_of_permission)

    def test_ModifyPortalContent_permission_roles(self):
        """
        'Modify portal content' permission should be given to 'Manager' role.
        """
        roles_of_permission = self.get_roles_of_permission('Modify portal content')
        self.assertTrue(len(roles_of_permission) == 1)
        self.assertTrue('Manager' in roles_of_permission)
