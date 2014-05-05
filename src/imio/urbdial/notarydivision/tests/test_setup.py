# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from imio.urbdial.notarydivision.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of imio.urbdial.notarydivision into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if imio.urbdial.notarydivision is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('imio.urbdial.notarydivision'))

    def test_uninstall(self):
        """Test if imio.urbdial.notarydivision is cleanly uninstalled."""
        self.installer.uninstallProducts(['imio.urbdial.notarydivision'])
        self.assertFalse(self.installer.isProductInstalled('imio.urbdial.notarydivision'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IImioUrbdialNotarydivisionLayer is registered."""
        from imio.urbdial.notarydivision.interfaces import IImioUrbdialNotarydivisionLayer
        from plone.browserlayer import utils
        self.assertIn(IImioUrbdialNotarydivisionLayer, utils.registered_layers())
