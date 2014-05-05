# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from imio.urbdial.notarydivision.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of imio.urbdial.notarydivision into Plone."""

    def test_portal_type_is_registered(self):
        portal_types = api.portal.get_tool("portal_types")
        registered_types = portal_types.listContentTypes()
        self.assertTrue('notarydivision' in registered_types)
