# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.testing import TEST_INSTALL_INTEGRATION

from plone import api

import unittest


class TestConfigFolder(unittest.TestCase):
    """
    """

    layer = TEST_INSTALL_INTEGRATION

    def test_ConfigFolder_portal_type_is_registered(self):
        portal_types = api.portal.get_tool('portal_types')
        registered_types = portal_types.listContentTypes()
        self.assertTrue('ConfigFolder' in registered_types)
