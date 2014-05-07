# -*- coding: utf-8 -*-
"""roles tests for this package."""

from imio.urbdial.notarydivision.testing import TEST_INSTALL_INTEGRATION
from plone.app.testing import applyProfile
from plone import api
import unittest


class TestRoles(unittest.TestCase):

    layer = TEST_INSTALL_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']

    def test_notaries_role_registration(self):
        """
        """
        portal_roles = self.portal.acl_users.portal_role_manager
        registered_roles = portal_roles.listRoleIds()
        self.assertTrue('NotaryDivision Creator' in registered_roles)
