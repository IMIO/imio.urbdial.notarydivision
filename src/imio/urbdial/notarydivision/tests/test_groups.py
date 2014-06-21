# -*- coding: utf-8 -*-
"""groups tests for this package."""

from imio.urbdial.notarydivision.testing import TEST_INSTALL_INTEGRATION
from plone import api
import unittest


class TestGroups(unittest.TestCase):

    layer = TEST_INSTALL_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']

    def test_notaries_group_creation(self):
        self.assertTrue(api.group.get('notaries'))

    def test_dgo4_group_creation(self):
        self.assertTrue(api.group.get('dgo4'))

    def test_townships_group_creation(self):
        self.assertTrue(api.group.get('townships'))
