# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from Acquisition import aq_base

from plone import api
from plone.app.testing import login

from imio.urbdial.notarydivision.testing import CommentBrowserTest
from imio.urbdial.notarydivision.testing import EXAMPLE_DIVISION_INTEGRATION
from imio.urbdial.notarydivision.testing import TEST_INSTALL_INTEGRATION
from imio.urbdial.notarydivision.testing import NotaryDivisionBrowserTest
from imio.urbdial.notarydivision.testing_vars import TEST_NOTARY_NAME

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

    def test_Observation_is_in_NotaryDivision_allowed_content_types(self):
        portal_types = api.portal.get_tool('portal_types')
        divnot_type = portal_types.NotaryDivision
        self.assertTrue('Observation' in divnot_type.allowed_content_types)

    def test_Precision_is_in_NotaryDivision_allowed_content_types(self):
        portal_types = api.portal.get_tool('portal_types')
        divnot_type = portal_types.NotaryDivision
        self.assertTrue('Precision' in divnot_type.allowed_content_types)

    def test_PrecisionDemand_is_in_NotaryDivision_allowed_content_types(self):
        portal_types = api.portal.get_tool('portal_types')
        divnot_type = portal_types.NotaryDivision
        self.assertTrue('PrecisionDemand' in divnot_type.allowed_content_types)

    def test_InadmissibleFolder_is_in_NotaryDivision_allowed_content_types(self):
        portal_types = api.portal.get_tool('portal_types')
        divnot_type = portal_types.NotaryDivision
        self.assertTrue('InadmissibleFolder' in divnot_type.allowed_content_types)


class TestNotaryDivisionFields(NotaryDivisionBrowserTest):
    """
    Test schema fields declaration.
    """

    layer = EXAMPLE_DIVISION_INTEGRATION

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

    def test_actual_use_attribute(self):
        test_divnot = aq_base(self.test_divnot)
        self.assertTrue(hasattr(test_divnot, 'actual_use'))

    def test_actual_use_field_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "field 'actual_use' is not displayed"
        self.assertTrue('id="form-widgets-actual_use"' in contents, msg)
        msg = "field 'actual_use' is not translated"
        self.assertTrue('Affectation actuelle du bien' in contents, msg)

    def test_actual_use_field_edit(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'actual_use' is not editable"
        self.assertTrue('Affectation actuelle du bien' in contents, msg)

    def test_initial_estate_attribute(self):
        test_divnot = aq_base(self.test_divnot)
        self.assertTrue(hasattr(test_divnot, 'initial_estate'))

    def test_initial_estate_field_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "field 'initial_estate' is not displayed"
        self.assertTrue('form.widgets.initial_estate' in contents, msg)
        msg = "field 'initial_estate' is not translated"
        self.assertTrue('Ensemble immobilier initial' in contents, msg)

    def test_initial_estate_field_edit(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents

        msg = "field 'initial_estate' is not editable"
        self.assertTrue('Ensemble immobilier initial' in contents, msg)

        datagrid_columns = [
            ('locality', 'Commune'),
            ('division', 'Division'),
            ('section', 'Section'),
            ('radical', 'Radical'),
            ('bis', 'Bis'),
            ('exposant', 'Exposant'),
            ('power', 'Puissance'),
            ('surface', 'Superficie'),
            ('specific_rights', 'Droits des parties'),
        ]
        for column_name, translation in datagrid_columns:
            msg = "column '{}' of 'initial_estate' field is not editable".format(column_name)
            self.assertTrue('id="form-widgets-initial_estate-AA-widgets-{}"'.format(column_name) in contents, msg)
            msg = "column '{}' of 'initial_estate' field is not translated".format(column_name)
            self.assertTrue(translation in contents, msg)

    def test_locality_field_vocabulary_displayed_for_initial_estate_field(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = 'Localities vocabulary not displayed in locality field of initial_estate'
        self.assertTrue('initial_estate-AA-widgets-locality-0" value="6250">Aiseau-Presles' in contents, msg)
        self.assertTrue('initial_estate-AA-widgets-locality-8" value="5000">Namur' in contents, msg)

    def test_created_estate_attribute(self):
        test_divnot = aq_base(self.test_divnot)
        self.assertTrue(hasattr(test_divnot, 'created_estate'))

    def test_created_estate_field_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = "field 'created_estate' is not displayed"
        self.assertTrue('form.widgets.created_estate' in contents, msg)
        msg = "field 'created_estate' is not translated"
        self.assertTrue('Ensemble immobilier créé' in contents, msg)

    def test_created_estate_field_edit(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents

        msg = "field 'created_estate' is not editable"
        self.assertTrue('Ensemble immobilier créé' in contents, msg)

        datagrid_columns = [
            ('locality', 'Commune'),
            ('division', 'Division'),
            ('section', 'Section'),
            ('radical', 'Radical'),
            ('bis', 'Bis'),
            ('exposant', 'Exposant'),
            ('power', 'Puissance'),
            ('surface_accuracy', '(type)'),
            ('surface', 'Superficie'),
            ('built', 'Bâti'),
            ('deed_type', 'Type d\'acte'),
            ('destination', 'Destination du lot'),
            ('specific_rights', 'Droits des parties'),
        ]
        for column_name, translation in datagrid_columns:
            msg = "column '{}' of 'created_estate' field is not editable".format(column_name)
            self.assertTrue('id="form-widgets-created_estate-AA-widgets-{}"'.format(column_name) in contents, msg)
            msg = "column '{}' of 'created_estate' field is not translated".format(column_name)
            self.assertTrue(translation in contents, msg)

    def test_locality_field_vocabulary_displayed_for_created_estate_field(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = 'Localities vocabulary not displayed in locality field of created_estate'
        self.assertTrue('created_estate-AA-widgets-locality-0" value="6250">Aiseau-Presles' in contents, msg)
        self.assertTrue('created_estate-AA-widgets-locality-8" value="5000">Namur' in contents, msg)

    def test_surface_accuracy_field_vocabulary_displayed_for_created_estate_field(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = 'Surface accuracy vocabulary not displayed in locality field of created_estate'
        self.assertTrue('created_estate-AA-widgets-surface_accuracy-0" value="cadastrale">' in contents, msg)
        self.assertTrue('created_estate-AA-widgets-surface_accuracy-1" value="mesuree">' in contents, msg)

    def test_deed_type_field_vocabulary_displayed_for_created_estate_field(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = 'Deed types vocabulary not displayed in locality field of created_estate'
        self.assertTrue('created_estate-AA-widgets-deed_type-0" value="vente">' in contents, msg)
        self.assertTrue('created_estate-AA-widgets-deed_type-1" value="partage">' in contents, msg)

    def test_article_90_attribute(self):
        test_divnot = aq_base(self.test_divnot)
        self.assertTrue(hasattr(test_divnot, 'article_90'))

    def test_article_90_field_display(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents

        msg = "field 'article_90' is not displayed"
        self.assertTrue('form-widgets-article_90' in contents, msg)
        msg = "field 'article_90' is not translated"
        self.assertTrue('Motifs d\'exception article 90' in contents, msg)

    def test_article_90_field_edit(self):
        self.browser.open(self.test_divnot.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'article_90' is not editable"
        self.assertTrue('Motifs d\'exception article 90' in contents, msg)

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
        self.assertTrue('Add Observation' in contents, msg)

    def test_NotaryDivision_addPrecision_buttons(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = 'test NotaryDivision AddPrecision button not appears in view'
        self.assertTrue('Add Precision' in contents, msg)

    def test_NotaryDivision_addPrecisionDemand_buttons(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = 'test NotaryDivision addPrecisionDemand button not appears in view'
        self.assertTrue('Add PrecisionDemand' in contents, msg)

    def test_NotaryDivision_addInadmissibleFolder_buttons(self):
        self.browser.open(self.test_divnot.absolute_url())
        contents = self.browser.contents
        msg = 'test NotaryDivision addInadmissibleFolder button not appears in view'
        self.assertTrue('Add InadmissibleFolder' in contents, msg)


class TestNotaryDivisionIntegration(CommentBrowserTest):
    """
    Integration tests of NotaryDivision
    """

    def test_published_comments_are_frozen_when_notarydivision_is_passed(self):
        notarydivision = self.test_divnot

        for comment in notarydivision.objectValues():
            api.content.transition(comment, 'Publish')

        for comment in notarydivision.objectValues():
            comment_state = api.content.get_state(comment)
            self.assertTrue(comment_state == 'Published')

        # 'Pass' notarydivision
        login(self.portal, TEST_NOTARY_NAME)
        api.content.transition(notarydivision, 'Pass')

        # Comments should be in Frozen states
        for comment in notarydivision.objectValues():
            comment_state = api.content.get_state(comment)
            msg = "Comment '{}' should be in state 'Frozen'".format(comment.id)
            self.assertTrue(comment_state == 'Frozen', msg)

    def test_published_comments_are_frozen_when_notarydivision_is_cancelled(self):
        notarydivision = self.test_divnot

        for comment in notarydivision.objectValues():
            api.content.transition(comment, 'Publish')

        for comment in notarydivision.objectValues():
            comment_state = api.content.get_state(comment)
            self.assertTrue(comment_state == 'Published')

        # 'Cancel' notarydivision
        login(self.portal, TEST_NOTARY_NAME)
        api.content.transition(notarydivision, 'Cancel')

        # Comments should be in Frozen states
        for comment in notarydivision.objectValues():
            comment_state = api.content.get_state(comment)
            msg = "Comment '{}' should be in state 'Frozen'".format(comment.id)
            self.assertTrue(comment_state == 'Frozen', msg)

    def test_draft_comments_are_deleted_when_notarydivision_is_passed(self):
        notarydivision = self.test_divnot

        for comment in notarydivision.objectValues():
            comment_state = api.content.get_state(comment)
            self.assertTrue(comment_state == 'Draft')

        login(self.portal, TEST_NOTARY_NAME)
        api.content.transition(notarydivision, 'Pass')
        msg = "Some draft comments are not deleted"
        self.assertTrue(len(notarydivision.objectValues()) == 0, msg)

    def test_draft_comments_are_deleted_when_notarydivision_is_cancelled(self):
        notarydivision = self.test_divnot

        for comment in notarydivision.objectValues():
            comment_state = api.content.get_state(comment)
            self.assertTrue(comment_state == 'Draft')

        login(self.portal, TEST_NOTARY_NAME)
        api.content.transition(notarydivision, 'Cancel')
        msg = "Some draft comments are not deleted"
        self.assertTrue(len(notarydivision.objectValues()) == 0, msg)
