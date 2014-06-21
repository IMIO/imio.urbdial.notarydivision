# -*- coding: utf-8 -*-
"""permissions tests for this package."""

from imio.urbdial.notarydivision.testing import TEST_INSTALL_INTEGRATION
from plone import api
import unittest


class TestRolesAndPermissions(unittest.TestCase):

    layer = TEST_INSTALL_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']

    def test_Member_role_is_assigned_to_notaries_group(self):
        roles_of_notaries_group = api.group.get_roles('notaries')
        self.assertTrue('Member' in roles_of_notaries_group)

    def test_Member_role_is_assigned_to_dgo4_group(self):
        roles_of_notaries_group = api.group.get_roles('notaries')
        self.assertTrue('Member' in roles_of_notaries_group)

    def test_Member_role_is_assigned_to_townships_group(self):
        roles_of_notaries_group = api.group.get_roles('notaries')
        self.assertTrue('Member' in roles_of_notaries_group)

    def test_ManageNotification_permission_registration(self):
        self.assertTrue('imio.urbdial.notarydivision: Manage notification' in self.portal.possible_permissions())

    def test_NotaryDivisionCreator_role_registration(self):
        portal_roles = self.portal.acl_users.portal_role_manager
        registered_roles = portal_roles.listRoleIds()
        self.assertTrue('NotaryDivision Creator' in registered_roles)

    def test_NotaryDivisionReader_role_regsitration(self):
        portal_roles = self.portal.acl_users.portal_role_manager
        registered_roles = portal_roles.listRoleIds()
        self.assertTrue('NotaryDivision Reader' in registered_roles)

    def test_NotaryDivisionManager_role_regsitration(self):
        portal_roles = self.portal.acl_users.portal_role_manager
        registered_roles = portal_roles.listRoleIds()
        self.assertTrue('NotaryDivision Manager' in registered_roles)

    def test_AddObservation_permission_registration(self):
        self.assertTrue('imio.urbdial.notarydivision: Add Observation' in self.portal.possible_permissions())

    def test_ObservationCreator_role_registration(self):
        portal_roles = self.portal.acl_users.portal_role_manager
        registered_roles = portal_roles.listRoleIds()
        self.assertTrue('Observation Creator' in registered_roles)

    def test_ObservationReader_role_registration(self):
        portal_roles = self.portal.acl_users.portal_role_manager
        registered_roles = portal_roles.listRoleIds()
        self.assertTrue('Observation Reader' in registered_roles)

    def test_ObservationManager_role_registration(self):
        portal_roles = self.portal.acl_users.portal_role_manager
        registered_roles = portal_roles.listRoleIds()
        self.assertTrue('Observation Manager' in registered_roles)

    def test_AddPrecision_permission_registration(self):
        self.assertTrue('imio.urbdial.notarydivision: Add Precision' in self.portal.possible_permissions())

    def test_PrecisionCreator_role_registration(self):
        portal_roles = self.portal.acl_users.portal_role_manager
        registered_roles = portal_roles.listRoleIds()
        self.assertTrue('Precision Creator' in registered_roles)

    def test_PrecisionReader_role_registration(self):
        portal_roles = self.portal.acl_users.portal_role_manager
        registered_roles = portal_roles.listRoleIds()
        self.assertTrue('Precision Reader' in registered_roles)

    def test_PrecisionManager_role_registration(self):
        portal_roles = self.portal.acl_users.portal_role_manager
        registered_roles = portal_roles.listRoleIds()
        self.assertTrue('Precision Manager' in registered_roles)
