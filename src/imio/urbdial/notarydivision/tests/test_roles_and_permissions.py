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
        self.assertTrue('imio.urbdial.notarydivision: AddObservation' in self.portal.possible_permissions())

    def test_ManageObservation_permission_registration(self):
        self.assertTrue('imio.urbdial.notarydivision: ManageObservation' in self.portal.possible_permissions())

    def test_ViewObservation_permission_registration(self):
        self.assertTrue('imio.urbdial.notarydivision: ViewObservation' in self.portal.possible_permissions())

    def test_ObservationCreator_role_registration(self):
        portal_roles = self.portal.acl_users.portal_role_manager
        registered_roles = portal_roles.listRoleIds()
        self.assertTrue('Observation Creator' in registered_roles)
