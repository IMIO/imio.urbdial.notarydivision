# -*- coding: utf-8 -*-
"""permissions tests for this package."""

from imio.urbdial.notarydivision.testing import TEST_INSTALL_INTEGRATION
from plone import api
import unittest


class TestRolesAndPermissions(unittest.TestCase):

    layer = TEST_INSTALL_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']

    def test_AddNotaryDivision_permission_registration(self):
        registered_permissions = self.portal.acl_users.possible_permissions()
        self.assertTrue('imio.urbdial.notarydivision: Add NotaryDivision' in registered_permissions)

    def test_NotaryDivisionCreator_role_registration(self):
        portal_roles = self.portal.acl_users.portal_role_manager
        registered_roles = portal_roles.listRoleIds()
        self.assertTrue('NotaryDivision Creator' in registered_roles)

    def test_add_NotaryDivision_rolemap(self):
        """
        'AddNotaryDivision' permission should be given to the 'NotaryDivision Creator' role
        """
        role_permissions = self.portal.permissionsOfRole('NotaryDivision Creator')
        permission_names = [p['name'] for p in role_permissions if p['selected']]
        self.assertTrue('imio.urbdial.notarydivision: Add NotaryDivision' in permission_names)
        self.assertTrue(len(permission_names) == 1)

    def test_EditNotaryDivision_permission_registration(self):
        registered_permissions = self.portal.acl_users.possible_permissions()
        self.assertTrue('imio.urbdial.notarydivision: Edit NotaryDivision' in registered_permissions)

    def test_Member_role_is_assigned_to_notaries_group(self):
        roles_of_notaries_group = api.group.get_roles('notaries')
        self.assertTrue('Member' in roles_of_notaries_group)
