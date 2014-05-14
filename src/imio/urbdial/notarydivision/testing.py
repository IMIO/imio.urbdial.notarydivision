# -*- coding: utf-8 -*-
"""Base module for unittesting."""

from plone import api
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing import z2

import imio.urbdial.notarydivision


class NakedPloneLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        self.loadZCML(package=imio.urbdial.notarydivision,
                      name='testing.zcml')
        z2.installProduct(app, 'imio.urbdial.notarydivision')

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'imio.urbdial.notarydivision')

NAKED_PLONE_FIXTURE = NakedPloneLayer(
    name="NAKED_PLONE_FIXTURE"
)

NAKED_PLONE_INTEGRATION = IntegrationTesting(
    bases=(NAKED_PLONE_FIXTURE,),
    name="NAKED_PLONE_INTEGRATION"
)


class TestInstallUrbdialLayer(NakedPloneLayer):

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        applyProfile(portal, 'imio.urbdial.notarydivision:testing')

        # Login and create some test content
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        # Commit so that the test browser sees these objects
        import transaction
        transaction.commit()

TEST_INSTALL_FIXTURE = TestInstallUrbdialLayer(
    name="TEST_INSTALL_FIXTURE"
)

TEST_INSTALL_INTEGRATION = IntegrationTesting(
    bases=(TEST_INSTALL_FIXTURE,),
    name="TEST_INSTALL_INTEGRATION"
)


TEST_INSTALL_FUNCTIONAL = FunctionalTesting(
    bases=(TEST_INSTALL_FIXTURE,),
    name="TEST_INSTALL_FUNCTIONAL"
)


class RealInstallUrbdialLayer(TestInstallUrbdialLayer):

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # apply plone default profile so we have default workflows on plone
        # content types and we can apply 'plone-content' profile without troubles
        applyProfile(portal, 'Products.CMFPlone:plone')
        applyProfile(portal, 'Products.CMFPlone:dependencies')
        # create plone root default objects
        applyProfile(portal, 'Products.CMFPlone:plone-content')
        applyProfile(portal, 'plonetheme.sunburst:default')
        # install urbdial.notarydivision
        super(RealInstallUrbdialLayer, self).setUpPloneSite(portal)

REAL_INSTALL_FIXTURE = RealInstallUrbdialLayer(
    name="REAL_INSTALL_FIXTURE"
)

REAL_INSTALL_INTEGRATION = IntegrationTesting(
    bases=(REAL_INSTALL_FIXTURE,),
    name="REAL_INSTALL_INTEGRATION"
)


REAL_INSTALL_FUNCTIONAL = FunctionalTesting(
    bases=(REAL_INSTALL_FIXTURE,),
    name="REAL_INSTALL_FUNCTIONAL"
)


ACCEPTANCE = FunctionalTesting(
    bases=(
        REAL_INSTALL_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name="ACCEPTANCE"
)


class ExampleDivisionLayer(TestInstallUrbdialLayer):

    def setUpPloneSite(self, portal):
        super(ExampleDivisionLayer, self).setUpPloneSite(portal)

        # Create some test content
        api.content.create(
            type='NotaryDivision',
            id='test_notarydivision',
            container=portal.notarydivisions,
        )

        # Commit so that the test browser sees these objects
        import transaction
        transaction.commit()


EXAMPLE_DIVISION_FIXTURE = ExampleDivisionLayer(
    name="EXAMPLE_DIVISION_FIXTURE"
)

EXAMPLE_DIVISION_INTEGRATION = IntegrationTesting(
    bases=(EXAMPLE_DIVISION_FIXTURE,),
    name="EXAMPLE_DIVISION_INTEGRATION"
)


EXAMPLE_DIVISION_FUNCTIONAL = FunctionalTesting(
    bases=(EXAMPLE_DIVISION_FIXTURE,),
    name="EXAMPLE_DIVISION_FUNCTIONAL"
)
