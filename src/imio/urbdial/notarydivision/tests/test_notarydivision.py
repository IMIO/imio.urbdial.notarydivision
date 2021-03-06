# -*- coding: utf-8 -*-

from Acquisition import aq_base

from DateTime import DateTime

from plone import api
from plone.app.testing import login

from imio.urbdial.notarydivision.testing import CommentBrowserTest
from imio.urbdial.notarydivision.testing import TEST_INSTALL_INTEGRATION
from imio.urbdial.notarydivision.testing import NotaryDivisionBrowserTest
from imio.urbdial.notarydivision.testing import NotaryDivisionFunctionalBrowserTest
from imio.urbdial.notarydivision.testing_vars import TEST_NOTARY_NAME
from imio.urbdial.notarydivision.utils import translate

import transaction

import unittest


class TestNotaryDivision(unittest.TestCase):
    """
    """

    layer = TEST_INSTALL_INTEGRATION

    def test_NotaryDivision_portal_type_is_registered(self):
        portal_types = api.portal.get_tool('portal_types')
        registered_types = portal_types.listContentTypes()
        self.assertTrue('NotaryDivision' in registered_types)

    def test_creation_permission_is_cmfAddPortalContent(self):
        portal_types = api.portal.get_tool('portal_types')
        divnot_type = portal_types.NotaryDivision
        self.assertTrue(divnot_type.add_permission == 'cmf.AddPortalContent')

    def test_CreatedParcelling_is_in_NotaryDivision_allowed_content_types(self):
        portal_types = api.portal.get_tool('portal_types')
        divnot_type = portal_types.NotaryDivision
        self.assertTrue('CreatedParcelling' in divnot_type.allowed_content_types)

    def test_Precision_is_in_NotaryDivision_allowed_content_types(self):
        portal_types = api.portal.get_tool('portal_types')
        divnot_type = portal_types.NotaryDivision
        self.assertTrue('Precision' in divnot_type.allowed_content_types)

    def test_FDObservation_is_in_NotaryDivision_allowed_content_types(self):
        portal_types = api.portal.get_tool('portal_types')
        divnot_type = portal_types.NotaryDivision
        self.assertTrue('FDObservation' in divnot_type.allowed_content_types)

    def test_TownshipObservation_is_in_NotaryDivision_allowed_content_types(self):
        portal_types = api.portal.get_tool('portal_types')
        divnot_type = portal_types.NotaryDivision
        self.assertTrue('TownshipObservation' in divnot_type.allowed_content_types)

    def test_FDPrecisionDemand_is_in_NotaryDivision_allowed_content_types(self):
        portal_types = api.portal.get_tool('portal_types')
        divnot_type = portal_types.NotaryDivision
        self.assertTrue('FDPrecisionDemand' in divnot_type.allowed_content_types)

    def test_FDInadmissibleFolder_is_in_NotaryDivision_allowed_content_types(self):
        portal_types = api.portal.get_tool('portal_types')
        divnot_type = portal_types.NotaryDivision
        self.assertTrue('FDInadmissibleFolder' in divnot_type.allowed_content_types)

    def test_TownshipPrecisionDemand_is_in_NotaryDivision_allowed_content_types(self):
        portal_types = api.portal.get_tool('portal_types')
        divnot_type = portal_types.NotaryDivision
        self.assertTrue('TownshipPrecisionDemand' in divnot_type.allowed_content_types)

    def test_TownshipInadmissibleFolder_is_in_NotaryDivision_allowed_content_types(self):
        portal_types = api.portal.get_tool('portal_types')
        divnot_type = portal_types.NotaryDivision
        self.assertTrue('TownshipInadmissibleFolder' in divnot_type.allowed_content_types)


class TestNotaryDivisionFields(NotaryDivisionBrowserTest):
    """
    Test schema fields declaration.
    """

    def test_class_registration(self):
        from imio.urbdial.notarydivision.content.notarydivision import NotaryDivision
        self.assertTrue(self.test_divnot.__class__ == NotaryDivision)

    def test_schema_registration(self):
        portal_types = api.portal.get_tool('portal_types')
        divnot_type = portal_types.get(self.test_divnot.portal_type)
        self.assertTrue('INotaryDivision' in divnot_type.schema)

    def test_exclude_from_navigation_attribute(self):
        test_divnot = aq_base(self.test_divnot)
        self.assertTrue(hasattr(test_divnot, 'exclude_from_nav'))

    def test_exclude_from_navigation_field_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = 'field exclude_from_nav should be hidden in Display View'
        self.assertTrue('<span id="form-widgets-exclude_from_nav"' not in contents, msg)

    def test_exclude_from_navigation_field_edit(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = 'field exclude_from_nav should be hidden in Display View'
        self.assertTrue('<span class="label">Exclude from navigation</span>' not in contents, msg)

    def test_exclude_from_navigation_field_default_value_is_True(self):
        self.assertTrue(self.test_divnot.exclude_from_nav)

    def test_local_dgo4_attribute(self):
        test_divnot = aq_base(self.test_divnot)
        self.assertTrue(hasattr(test_divnot, 'local_dgo4'))

    def test_local_dgo4_field_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = 'field local_dgo4 should be visible in Display View'
        self.assertTrue('Direction(s) provinciale concernée(s)' in contents, msg)

    def test_local_dgo4_field_edit(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = 'field local_dgo4 should be hidden in edit'
        self.assertTrue('Direction(s) provinciale concernée(s)' not in contents, msg)

        self.browser.open(self.portal.absolute_url() + '/notarydivisions/++add++NotaryDivision')
        contents = self.browser.contents
        msg = 'field local_dgo4 should be hidden in add form'
        self.assertTrue('Direction(s) provinciale concernée(s)' not in contents, msg)

    def test_local_township_attribute(self):
        test_divnot = aq_base(self.test_divnot)
        self.assertTrue(hasattr(test_divnot, 'local_township'))

    def test_local_township_field_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = 'field local_township should be visible in Display View'
        self.assertTrue('Commune(s) concernée(s)' in contents, msg)

    def test_local_township_field_edit(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = 'field local_township should be hidden in edit'
        self.assertTrue('Commune(s) concernée(s)' not in contents, msg)

        self.browser.open(self.portal.absolute_url() + '/notarydivisions/++add++NotaryDivision')
        contents = self.browser.contents
        msg = 'field local_township should be hidden in add form'
        self.assertTrue('Commune(s) concernée(s)' not in contents, msg)

    def test_reference_attribute(self):
        test_divnot = aq_base(self.test_divnot)
        self.assertTrue(hasattr(test_divnot, 'reference'))

    def test_reference_field_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "field 'reference' is not displayed"
        self.assertTrue('id="form-widgets-reference"' in contents, msg)
        msg = "field 'reference' is not translated"
        self.assertTrue('Référence' in contents, msg)

    def test_reference_field_edit(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'reference' is not editable"
        self.assertTrue('Référence' in contents, msg)

    def test_applicants_attribute(self):
        test_divnot = aq_base(self.test_divnot)
        self.assertTrue(hasattr(test_divnot, 'applicants'))

    def test_applicants_field_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents

        msg = "field 'applicants' is not displayed"
        self.assertTrue('form.widgets.applicants' in contents, msg)
        msg = "field 'applicants' is not translated"
        self.assertTrue('Requérant(s)' in contents, msg)
        self.assertTrue('Nom' in contents)
        self.assertTrue('Prénom' in contents)

    def test_applicants_field_edit(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'applicants' is not editable"
        self.assertTrue('Requérant(s)' in contents, msg)

        datagrid_columns = [
            ('firstname', 'Prénom'),
            ('name', 'Nom'),
        ]
        for column_name, translation in datagrid_columns:
            msg = "column '{}' of 'applicants' field is not editable".format(column_name)
            self.assertTrue('<input id="form-widgets-applicants-AA-widgets-{}"'.format(column_name) in contents, msg)
            msg = "column '{}' of 'applicants' field is not translated".format(column_name)
            self.assertTrue(translation in contents, msg)

    def test_article_90_attribute(self):
        test_divnot = aq_base(self.test_divnot)
        self.assertTrue(hasattr(test_divnot, 'article_90'))

    def test_article_90_field_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents

        msg = "field 'article_90' is not displayed"
        self.assertTrue('form-widgets-article_90' in contents, msg)
        msg = "field 'article_90' is not translated"
        self.assertTrue('Cette division entre dans le champ de l’article 90' in contents, msg)

    def test_article_90_field_edit(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'article_90' is not editable"
        self.assertTrue('Cette division entre dans le champ de l’article 90' in contents, msg)

    def test_article_90_field_vocabulary_is_displayed(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = 'Article 90 vocabulary not displayed'
        self.assertTrue('1° : la division résulte d\'un ou plusieurs acte(s) de donation' in contents, msg)
        self.assertTrue('2° : la division résulte d\'un ou plusieurs acte(s) involontaire(s)' in contents, msg)

    def test_article90_detail_attribute(self):
        test_divnot = aq_base(self.test_divnot)
        self.assertTrue(hasattr(test_divnot, 'article90_detail'))

    def test_article90_detail_field_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents

        msg = "field 'article90_detail' is not displayed"
        self.assertTrue('form-widgets-article90_detail' in contents, msg)
        msg = "field 'article90_detail' is not translated"
        self.assertTrue('Justificatif des motifs d\'exception' in contents, msg)

    def test_article90_detail_field_edit(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'article90_detail' is not editable"
        self.assertTrue('Justificatif des motifs d\'exception' in contents, msg)

    def test_plan_reference_attribute(self):
        test_divnot = aq_base(self.test_divnot)
        self.assertTrue(hasattr(test_divnot, 'plan_reference'))

    def test_plan_reference_field_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents

        msg = "field 'plan_reference' is not displayed"
        self.assertTrue('form-widgets-plan_reference' in contents, msg)
        msg = "field 'plan_reference' is not translated"
        self.assertTrue('Référence du plan' in contents, msg)

    def test_plan_reference_field_edit(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'plan_reference' is not editable"
        self.assertTrue('Référence du plan' in contents, msg)

    def test_plan_date_attribute(self):
        test_divnot = aq_base(self.test_divnot)
        self.assertTrue(hasattr(test_divnot, 'plan_date'))

    def test_plan_date_field_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents

        msg = "field 'plan_date' is not displayed"
        self.assertTrue('form-widgets-plan_date' in contents, msg)
        msg = "field 'plan_date' is not translated"
        self.assertTrue('Date du plan' in contents, msg)

    def test_plan_date_field_edit(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'plan_date' is not editable"
        self.assertTrue('Date du plan' in contents, msg)

    def test_geometrician_attribute(self):
        test_divnot = aq_base(self.test_divnot)
        self.assertTrue(hasattr(test_divnot, 'geometrician'))

    def test_geometrician_field_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents

        msg = "field 'geometrician' is not displayed"
        self.assertTrue('form-widgets-geometrician' in contents, msg)
        msg = "field 'geometrician' is not translated"
        self.assertTrue('Géomètre' in contents, msg)

    def test_geometrician_field_edit(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'geometrician' is not editable"
        self.assertTrue('Géomètre' in contents, msg)

    def test_plan_files_attribute(self):
        test_divnot = aq_base(self.test_divnot)
        self.assertTrue(hasattr(test_divnot, 'plan_files'))

    def test_plan_files_field_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "field 'plan_files' is not displayed (or not translated)"
        self.assertTrue('Fichiers (plan)' in contents, msg)

    def test_plan_files_field_edit(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'plan_files' is not editable"
        self.assertTrue('Fichiers (plan)' in contents, msg)

    def test_annex_files_attribute(self):
        test_divnot = aq_base(self.test_divnot)
        self.assertTrue(hasattr(test_divnot, 'annex_files'))

    def test_annex_files_field_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "field 'annex_files' is not displayed (or not translated)"
        self.assertTrue('Fichiers des annexes' in contents, msg)

    def test_annex_files_field_edit(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'annex_files' is not editable"
        self.assertTrue('Fichiers des annexes' in contents, msg)

    def test_entrusting_attribute(self):
        test_divnot = aq_base(self.test_divnot)
        self.assertTrue(hasattr(test_divnot, 'entrusting'))

    def test_entrusting_field_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "field 'entrusting' displayed and should be hidden"
        self.assertTrue('Sauf en cas de force majeure' not in contents, msg)

    def test_entrusting_field_edit(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'entrusting' is not editable"
        self.assertTrue('Sauf en cas de force majeure' in contents, msg)

    def test_entrusting_field_is_required(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        pass


class TestAddNotaryDivision(NotaryDivisionBrowserTest):
    """
    Test NotaryDivision Add form.
    """

    def test_NotaryDivisionAddForm_class_registration(self):
        from imio.urbdial.notarydivision.content.notarydivision_view import NotaryDivisionAddForm
        add_form = self.portal.notarydivisions.restrictedTraverse('++add++NotaryDivision')
        self.assertTrue(add_form.form == NotaryDivisionAddForm)


class TestNotaryDivisionEdit(NotaryDivisionBrowserTest):
    """
    Test NotaryDivision Edit form.
    """

    def test_NotaryDivisionEditForm_class_registration(self):
        from imio.urbdial.notarydivision.content.notarydivision_view import NotaryDivisionEditForm
        edit = self.test_divnot.restrictedTraverse('@@edit')
        self.assertTrue(isinstance(edit, NotaryDivisionEditForm))


class TestNotaryDivisionView(NotaryDivisionBrowserTest):
    """
    Test NotaryDivision View.
    """

    def test_NotaryDivisionView_class_registration(self):
        from imio.urbdial.notarydivision.content.notarydivision_view import NotaryDivisionView
        view = self.test_divnot.restrictedTraverse('view')
        self.assertTrue(isinstance(view, NotaryDivisionView))

    def test_NotaryDivision_excluded_from_navigation(self):
        self.browser.open(self.portal.absolute_url())
        contents = self.browser.contents
        msg = 'test NotaryDivision appears in navigation bar'
        self.assertTrue('<li id="portaltab-test_notarydivision" class="plain">' not in contents, msg)

    def test_view_template_customize_body_slot_of_Plone_main_template(self):
        """
        The 'Last modification' link should not appears.
        """
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = 'Last modification link is still visible.'
        self.assertTrue('<span class="documentAuthor">' not in contents, msg)
        self.assertTrue('<span class="documentModified">' not in contents, msg)

    def test_NotaryDivision_addObservation_buttons(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = 'test NotaryDivision addObservation button not appears in view'
        addObservation = ''.format(
            translate(u'Add'),
            translate(u'Observation').encode('utf-8')
        )
        self.assertTrue(addObservation in contents, msg)

    def test_NotaryDivision_addPrecision_buttons(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = 'test NotaryDivision AddPrecision button not appears in view'
        addPrecision = ''.format(
            translate(u'Add'),
            translate(u'Precision').encode('utf-8')
        )
        self.assertTrue(addPrecision in contents, msg)

    def test_NotaryDivision_addPrecisionDemand_buttons(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = 'test NotaryDivision addPrecisionDemand button not appears in view'
        addPrecisionDemand = ''.format(
            translate(u'Add'),
            translate(u'PrecisionDemand').encode('utf-8')
        )
        self.assertTrue(addPrecisionDemand in contents, msg)

    def test_NotaryDivision_addInadmissibleFolder_buttons(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = 'test NotaryDivision addInadmissibleFolder button not appears in view'
        addInadmissibleFolder = ''.format(
            translate(u'Add'),
            translate(u'InadmissibleFolder').encode('utf-8')
        )
        self.assertTrue(addInadmissibleFolder in contents, msg)

    def test_NotaryDivision_empty_title(self):
        divnot = self.test_divnot
        expected_title = ' -  (Sambreville)'
        msg = 'expected title: "{}" but got "{}"'.format(expected_title, divnot.title)
        self.assertTrue(expected_title == divnot.title, msg)

    def test_NotaryDivision_title(self):
        divnot = self.test_divnot
        divnot.reference = 'REF 666'
        divnot.applicants = [
            {'name': 'Delcourt', 'firstname': 'Simon'},
            {'name': 'Antoine', 'firstname': 'Vivian'},
        ]

        expected_title = 'REF 666 - DELCOURT, ANTOINE (Sambreville)'
        msg = 'expected title: "{}" but got "{}"'.format(expected_title, divnot.title)
        self.assertTrue(expected_title == divnot.title, msg)


class TestFunctionnalNotaryDivisionView(NotaryDivisionFunctionalBrowserTest):
    """
    Functionnal tests of NotaryDivision View.
    """

    def test_NotaryDivision_title_display(self):
        divnot = self.test_divnot
        divnot.reference = 'REF 666'
        transaction.commit()

        self.browser.open(divnot.absolute_url())
        contents = self.browser.contents
        msg = 'title "{}" is not visible on notarydivision view'.format(divnot.title)
        self.assertTrue(divnot.title in contents, msg)

    def test_NotaryDivision_address_display(self):
        self.test_divnot.street = u'rue du pré'
        self.test_divnot.street_number = u'42'
        transaction.commit()

        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        expected_address = '42, rue du pré'
        msg = 'expected address display: "{}"'.format(expected_address)
        self.assertTrue(expected_address in contents, msg)

    def test_NotaryDivision_street_number_display(self):
        self.test_divnot.street_number = u'42'
        transaction.commit()

        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        self.assertTrue('42,' not in contents)
        self.assertTrue('42' in contents)

    def test_NotaryDivision_street_display(self):
        self.test_divnot.street = u'rue du pré'
        transaction.commit()

        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        self.assertTrue(', rue du pré' not in contents)
        self.assertTrue('rue du pré' in contents)


class TestNotaryDivisionMethods(NotaryDivisionBrowserTest):
    """
    Test NotaryDivision methods.
    """

    def test_get_notification_date(self):
        notarydivision = self.test_divnot

        # So far, no notification date.
        self.assertTrue(notarydivision.is_in_draft())
        self.assertTrue(notarydivision.get_notification_date() is None)

        # Notify
        notarydivision.transition('Notify')
        now = DateTime()
        notification_date = notarydivision.get_notification_date()
        msg = "Notification date should exists."
        self.assertTrue(notification_date, msg)
        msg = "Delta bewteen now and notification_date should be < to 1 sec"
        self.assertTrue(now - notification_date < 1, msg)

    def test_is_passed(self):
        notarydivision = self.test_divnot
        self.assertTrue(not notarydivision.is_passed())

        notarydivision.transition('Notify')
        notarydivision.transition('Pass')

        self.assertTrue(notarydivision.is_passed())

    def test_get_passed_date(self):
        notarydivision = self.test_divnot

        # So far, no passed date.
        self.assertTrue(notarydivision.is_in_draft())
        self.assertTrue(notarydivision.get_notification_date() is None)

        # Pass the notarydivision
        notarydivision.transition('Notify')
        notarydivision.transition('Pass')
        expected_date = '1986/09/18 14:43:40.171069 GMT+2'
        state_history = notarydivision.workflow_history.values()[0][-1]
        state_history['comments'] = expected_date

        passed_date = notarydivision.get_passed_date()
        msg = "Passed date should exists."
        self.assertTrue(passed_date, msg)
        self.assertTrue(passed_date == DateTime(expected_date))


class TestNotaryDivisionIntegration(CommentBrowserTest):
    """
    Integration tests of NotaryDivision
    """

    def test_published_comments_are_frozen_when_notarydivision_is_passed(self):
        notarydivision = self.test_divnot

        for comment in notarydivision.get_comments():
            comment.transition('Publish')

        # 'Pass' notarydivision
        login(self.portal, TEST_NOTARY_NAME)
        notarydivision.transition('Pass')

        # Comments should be in Frozen states
        for comment in notarydivision.get_comments():
            msg = "Comment '{}' should be in state 'Frozen'".format(comment.id)
            self.assertTrue(comment.is_frozen(), msg)

    def test_published_comments_are_frozen_when_notarydivision_is_cancelled(self):
        notarydivision = self.test_divnot

        for comment in notarydivision.get_comments():
            comment.transition('Publish')

        # 'Cancel' notarydivision
        login(self.portal, TEST_NOTARY_NAME)
        notarydivision.transition('CancelAct')

        # Comments should be in Frozen states
        for comment in notarydivision.get_comments():
            msg = "Comment '{}' should be in state 'Frozen'".format(comment.id)
            self.assertTrue(comment.is_frozen(), msg)

    def test_draft_comments_are_deleted_when_notarydivision_is_passed(self):
        notarydivision = self.test_divnot

        for comment in notarydivision.get_comments():
            self.assertTrue(comment.is_in_draft())

        login(self.portal, TEST_NOTARY_NAME)
        notarydivision.transition('Pass')
        msg = "Some draft comments are not deleted"
        self.assertTrue(len(notarydivision.get_comments()) == 0, msg)

    def test_draft_comments_are_deleted_when_notarydivision_is_cancelled(self):
        notarydivision = self.test_divnot

        for comment in notarydivision.get_comments():
            self.assertTrue(comment.is_in_draft())

        login(self.portal, TEST_NOTARY_NAME)
        notarydivision.transition('CancelAct')
        msg = "Some draft comments are not deleted"
        self.assertTrue(len(notarydivision.get_comments()) == 0, msg)
