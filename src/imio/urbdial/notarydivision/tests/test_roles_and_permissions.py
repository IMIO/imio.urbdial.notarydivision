# -*- coding: utf-8 -*-
"""permissions tests for this package."""

from imio.urbdial.notarydivision.testing import TEST_INSTALL_INTEGRATION
from plone import api
import unittest


class TestRolesAndPermissions(unittest.TestCase):

    layer = TEST_INSTALL_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']

    def test_NotaryDivisionCreator_role_registration(self):
        portal_roles = self.portal.acl_users.portal_role_manager
        registered_roles = portal_roles.listRoleIds()
        self.assertTrue('NotaryDivision Creator' in registered_roles)

    def test_add_NotaryDivision_rolemap(self):
        """
        'cmf.AddPortalContent' permission should be given to the 'NotaryDivision Creator' role
        """
        role_permissions = self.portal.rolesOfPermission('Add portal content')
        role_names = [p['name'] for p in role_permissions if p['selected']]
        self.assertTrue('NotaryDivision Creator' in role_names)

    def test_Member_role_is_assigned_to_notaries_group(self):
        roles_of_notaries_group = api.group.get_roles('notaries')
        self.assertTrue('Member' in roles_of_notaries_group)

    def test_AddObservation_permission_registration(self):
        self.assertTrue('imio.urbdial.notarydivision: Add Observation' in self.portal.possible_permissions())

    def test_ObservationCreator_role_registration(self):
        portal_roles = self.portal.acl_users.portal_role_manager
        registered_roles = portal_roles.listRoleIds()
        self.assertTrue('Observation Creator' in registered_roles)

    def test_add_Observation_rolemap(self):
        """
        'AddObservation' permission should be given to the 'Observation Creator' role
        """
        role_permissions = self.portal.rolesOfPermission('imio.urbdial.notarydivision: Add Observation')
        role_names = [p['name'] for p in role_permissions if p['selected']]
        self.assertTrue('Observation Creator' in role_names)

    def test_ObservationReader_role_registration(self):
        portal_roles = self.portal.acl_users.portal_role_manager
        registered_roles = portal_roles.listRoleIds()
        self.assertTrue('Observation Reader' in registered_roles)

    def test_view_Observation_rolemap(self):
        """
        'View' permission should be given to the 'Observation Reader' role
        """
        role_permissions = self.portal.rolesOfPermission('View')
        role_names = [p['name'] for p in role_permissions if p['selected']]
        self.assertTrue('Observation Reader' in role_names)

    def test_ObservationManager_role_registration(self):
        portal_roles = self.portal.acl_users.portal_role_manager
        registered_roles = portal_roles.listRoleIds()
        self.assertTrue('Observation Manager' in registered_roles)

    def test_manage_Observation_rolemap(self):
        """
        'Delete' and 'Edit' permissions should be given to the 'Observation Manager' role
        """
        role_permissions = self.portal.rolesOfPermission('Modify portal content')
        role_names = [p['name'] for p in role_permissions if p['selected']]
        self.assertTrue('Observation Manager' in role_names)

        role_permissions = self.portal.rolesOfPermission('Delete objects')
        role_names = [p['name'] for p in role_permissions if p['selected']]
        self.assertTrue('Observation Manager' in role_names)

    def test_AddPrecision_permission_registration(self):
        self.assertTrue('imio.urbdial.notarydivision: Add Precision' in self.portal.possible_permissions())

    def test_PrecisionCreator_role_registration(self):
        portal_roles = self.portal.acl_users.portal_role_manager
        registered_roles = portal_roles.listRoleIds()
        self.assertTrue('Precision Creator' in registered_roles)

    def test_add_precision_rolemap(self):
        """
        'AddPrecision' permission should be given to the 'Precision Creator' role
        """
        role_permissions = self.portal.rolesOfPermission('imio.urbdial.notarydivision: Add Precision')
        role_names = [p['name'] for p in role_permissions if p['selected']]
        self.assertTrue('Precision Creator' in role_names)

    def test_PrecisionReader_role_registration(self):
        portal_roles = self.portal.acl_users.portal_role_manager
        registered_roles = portal_roles.listRoleIds()
        self.assertTrue('Precision Reader' in registered_roles)

    def test_view_precision_rolemap(self):
        """
        'View' permission should be given to the 'Precision Reader' role
        """
        role_permissions = self.portal.rolesOfPermission('View')
        role_names = [p['name'] for p in role_permissions if p['selected']]
        self.assertTrue('Precision Reader' in role_names)

    def test_PrecisionManager_role_registration(self):
        portal_roles = self.portal.acl_users.portal_role_manager
        registered_roles = portal_roles.listRoleIds()
        self.assertTrue('Precision Manager' in registered_roles)

    def test_manage_precision_rolemap(self):
        """
        'Delete' and 'Edit' permissions should be given to the 'Precision Manager' role
        """
        role_permissions = self.portal.rolesOfPermission('Modify portal content')
        role_names = [p['name'] for p in role_permissions if p['selected']]
        self.assertTrue('Precision Manager' in role_names)

        role_permissions = self.portal.rolesOfPermission('Delete objects')
        role_names = [p['name'] for p in role_permissions if p['selected']]
        self.assertTrue('Precision Manager' in role_names)
