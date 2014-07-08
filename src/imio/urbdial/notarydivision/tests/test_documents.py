# -*- coding: utf-8 -*-

from collective.documentgenerator.content.condition import IPODTemplateCondition

from imio.urbdial.notarydivision.testing import CommentBrowserTest
from imio.urbdial.notarydivision.testing import TEST_INSTALL_INTEGRATION
from imio.urbdial.notarydivision.testing_vars import TEST_FD_NAME
from imio.urbdial.notarydivision.testing_vars import TEST_FD_PASSWORD
from imio.urbdial.notarydivision.testing_vars import TEST_NOTARY_NAME
from imio.urbdial.notarydivision.testing_vars import TEST_NOTARY_PASSWORD
from imio.urbdial.notarydivision.testing_vars import TEST_TOWNSHIP_NAME

from imio.urbdial.notarydivision.utils import get_pod_templates_folder

from plone import api
from plone.app.testing import login

from zope.component import queryMultiAdapter

import unittest


class TestInstall(unittest.TestCase):
    """
    Test portal_types install.
    """

    layer = TEST_INSTALL_INTEGRATION

    def test_templates_creation(self):
        expected_template_ids = set(
            (
                'notification-fd', 'notification-ac',
                'precision-fd', 'precision-ac',
                'acte-passe-fd', 'acte-passe-ac',
            )
        )
        templates_folder = get_pod_templates_folder()
        template_ids = set(templates_folder.objectIds())

        self.assertTrue(expected_template_ids == template_ids)


class TestDocumentConditions(CommentBrowserTest):
    """
    Test documents generation conditions.
    """

    def get_pod_template(self, template_id):
        templates_folder = get_pod_templates_folder()
        return getattr(templates_folder, template_id)

    def get_template_condition(self, template_id, context=None):
        if not context:
            context = self.test_divnot
        pod_template = self.get_pod_template(template_id)
        condition_name = pod_template.condition_adapter
        condition_obj = queryMultiAdapter((pod_template, context), IPODTemplateCondition, condition_name)
        return condition_obj

    def test_notification_condition_registration(self):
        from imio.urbdial.notarydivision.content.template_conditions import NotificationDocumentCondition

        template_id = 'notification-fd'
        condition_obj = self.get_template_condition(template_id)

        msg = "Condition of template {} should be an instance of NotificationDocumentCondition".format(template_id)
        self.assertTrue(isinstance(condition_obj, NotificationDocumentCondition), msg)

        template_id = 'notification-ac'
        condition_obj = self.get_template_condition(template_id)

        msg = "Condition of template {} should be an instance of NotificationDocumentCondition".format(template_id)
        self.assertTrue(isinstance(condition_obj, NotificationDocumentCondition), msg)

    def test_notification_condition(self):
        """
        Notification document condition should be True when:
        -The notarydivision is at least notified.
        """

        notarydivision = self.test_divnot
        template_id = 'notification-fd'

        # put the notarydivision in preparation state and login with a notary
        # user. The condition should be False.
        api.content.transition(notarydivision, 'Pass')
        api.content.transition(notarydivision, 'Restart')
        self.assertTrue(api.content.get_state(notarydivision) == 'In preparation')
        login(self.portal, TEST_NOTARY_NAME)

        condition_obj = self.get_template_condition(template_id)
        msg = "No notification document generation should be available when notarydivision is in preparation state."
        self.assertTrue(condition_obj.evaluate() is False, msg)

        # put the notarydivision in investigation state. Stay with notary user.
        # The condition should be True.
        api.content.transition(notarydivision, 'Notify')

        condition_obj = self.get_template_condition(template_id)
        msg = "Notification document should be available for generation"
        self.assertTrue(condition_obj.evaluate() is True, msg)

        # Switch to a non notary user. The condition should be False.
        login(self.portal, TEST_FD_NAME)

        condition_obj = self.get_template_condition(template_id)
        msg = "No notification document generation should be available for non notary user."
        self.assertTrue(condition_obj.evaluate() is False, msg)

    def test_act_passed_condition_registration(self):
        from imio.urbdial.notarydivision.content.template_conditions import PassedDocumentCondition

        template_id = 'acte-passe-fd'
        condition_obj = self.get_template_condition(template_id)

        msg = "Condition of template {} should be an instance of PassedDocumentCondition".format(template_id)
        self.assertTrue(isinstance(condition_obj, PassedDocumentCondition), msg)

        template_id = 'acte-passe-ac'
        condition_obj = self.get_template_condition(template_id)

        msg = "Condition of template {} should be an instance of PassedDocumentCondition".format(template_id)
        self.assertTrue(isinstance(condition_obj, PassedDocumentCondition), msg)

    def test_act_passed_condition(self):
        """
        Notification document condition should be True when:
        -The notarydivision is in passed state.
        """

        notarydivision = self.test_divnot
        template_id = 'acte-passe-fd'

        # The notarydivision is not in passed state. The condition should be False.
        login(self.portal, TEST_NOTARY_NAME)
        condition_obj = self.get_template_condition(template_id)
        msg = "No act passed document generation should be available when notarydivision is not in passed state."
        self.assertTrue(condition_obj.evaluate() is False, msg)

        # put the notarydivision in passed state. Stay with notary user.
        # The condition should be True.
        api.content.transition(notarydivision, 'Pass')
        condition_obj = self.get_template_condition(template_id)
        msg = "Act passed document should be available for generation"
        self.assertTrue(condition_obj.evaluate() is True, msg)

        # Switch to a non notary user. The condition should be False.
        login(self.portal, TEST_FD_NAME)
        condition_obj = self.get_template_condition(template_id)
        msg = "No notification document generation should be available for non notary user."
        self.assertTrue(condition_obj.evaluate() is False, msg)

    def test_fd_precision_condition_registration(self):
        from imio.urbdial.notarydivision.content.template_conditions import PrecisionFDDocumentCondition

        template_id = 'precision-fd'
        condition_obj = self.get_template_condition(template_id)

        msg = "Condition should be an instance of PrecisionFDDocumentCondition"
        self.assertTrue(isinstance(condition_obj, PrecisionFDDocumentCondition), msg)

    def test_fd_precision_condition(self):
        """
        Precision fd document condition should be True when:
        -The answered comment was written by a FD.
        -The precision is at least published.
        """

        template_id = 'precision-fd'
        observation = self.test_observation
        # publish the FD observation and create a precision on it.
        login(self.portal, TEST_FD_NAME)
        api.content.transition(observation, 'Publish')
        login(self.portal, TEST_NOTARY_NAME)
        precision = api.content.create(type='Precision', id='precision', container=observation)

        # The precision is not published. The condition should False.
        condition_obj = self.get_template_condition(template_id, context=precision)
        msg = "No document generation should be available for a precision in draft."
        self.assertTrue(condition_obj.evaluate() is False, msg)

        # Publish the precision, The condition should be True.
        api.content.transition(precision, 'Publish')
        condition_obj = self.get_template_condition(template_id, context=precision)
        msg = "Precision document generation should be available."
        self.assertTrue(condition_obj.evaluate() is True, msg)

        # Switch to a non notary user. The condition should be False.
        login(self.portal, TEST_FD_NAME)
        condition_obj = self.get_template_condition(template_id, context=precision)
        msg = "No document generation should be available for a non notary user."
        self.assertTrue(condition_obj.evaluate() is False, msg)

        # If the author of the answered comment is not a FD , condition should
        # be False
        login(self.portal, TEST_NOTARY_NAME)
        observation.is_dgo4_or_township = lambda: 'townships'
        condition_obj = self.get_template_condition(template_id, context=precision)
        msg = "Precision fd document should available only if previous comment author is FD."
        self.assertTrue(condition_obj.evaluate() is False, msg)

    def test_ac_precision_condition_registration(self):
        from imio.urbdial.notarydivision.content.template_conditions import PrecisionACDocumentCondition

        template_id = 'precision-ac'
        condition_obj = self.get_template_condition(template_id)

        msg = "Condition should be an instance of PrecisionACDocumentCondition"
        self.assertTrue(isinstance(condition_obj, PrecisionACDocumentCondition), msg)

    def test_ac_precision_condition(self):
        """
        Precision ac document condition should be True when:
        -The answered comment was written by a FD.
        -The precision is at least published.
        """

        template_id = 'precision-ac'
        observation = self.test_observation
        # create and publish a township observation then create a precision on it.
        login(self.portal, TEST_TOWNSHIP_NAME)
        observation = api.content.create(type='Observation', id='obs', container=self.test_divnot)
        api.content.transition(observation, 'Publish')
        login(self.portal, TEST_NOTARY_NAME)
        precision = api.content.create(type='Precision', id='precision', container=observation)

        # The precision is not published. The condition should False.
        condition_obj = self.get_template_condition(template_id, context=precision)
        msg = "No document generation should be available for a precision in draft."
        self.assertTrue(condition_obj.evaluate() is False, msg)

        # Publish the precision, The condition should be True.
        api.content.transition(precision, 'Publish')
        condition_obj = self.get_template_condition(template_id, context=precision)
        msg = "Precision document generation should be available."
        self.assertTrue(condition_obj.evaluate() is True, msg)

        # Switch to a non notary user. The condition should be False.
        login(self.portal, TEST_FD_NAME)
        condition_obj = self.get_template_condition(template_id, context=precision)
        msg = "No document generation should be available for a non notary user."
        self.assertTrue(condition_obj.evaluate() is False, msg)

        # If the author of the answered comment is not from townships, condition should
        # be False
        login(self.portal, TEST_NOTARY_NAME)
        observation.is_dgo4_or_township = lambda: 'dgo4'
        condition_obj = self.get_template_condition(template_id, context=precision)
        msg = "Precision ac document should available only if previous comment author is from townships."
        self.assertTrue(condition_obj.evaluate() is False, msg)


class TestDocumentActions(CommentBrowserTest):
    """
    Test iconified document generation actions.
    """

    def test_document_action_display_on_notarydivision(self):
        """
        When the condition of a PODTemplate is matched, the link to generate the
        document should appears on the notarydivision view.
        """
        template_id = 'notification-fd'
        templates_folder = get_pod_templates_folder()
        template = getattr(templates_folder, template_id)
        notarydivision = self.test_divnot
        self.browser_login(TEST_NOTARY_NAME, TEST_NOTARY_PASSWORD)

        # If the template can be generated, the generation action should be visible.
        self.assertTrue(template.can_be_generated(notarydivision))
        self.browser.open(notarydivision.absolute_url())
        msg = "Document generation action for notification (FD) document should be visible."
        self.assertTrue('Notification (FD)</a>' in self.browser.contents, msg)

        self.browser_login(TEST_FD_NAME, TEST_FD_PASSWORD)
        # If the template cannot be generated, the generation action should not be there.
        self.assertTrue(not template.can_be_generated(notarydivision))
        self.browser.open(notarydivision.absolute_url())
        msg = "Document generation action for notification (FD) document should not be visible."
        self.assertTrue('Notification (FD)</a>' not in self.browser.contents, msg)
