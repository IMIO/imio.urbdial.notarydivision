# -*- coding: utf-8 -*-

from DateTime import DateTime

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow

from imio.urbdial.notarydivision import _
from imio.urbdial.notarydivision.browser.parcel_datagridfield import ParcelDataGridFieldFactory
from imio.urbdial.notarydivision.content.base import UrbdialContainer
from imio.urbdial.notarydivision.content.comment import IComment
from imio.urbdial.notarydivision.content.parcel import IParcel
from imio.urbdial.notarydivision.content.interfaces import INotaryDivisionElement
from imio.urbdial.notarydivision.testing_vars import TEST_FD_LOCALGROUP
from imio.urbdial.notarydivision.testing_vars import TEST_TOWNSHIP_LOCALGROUP

from plone import api
from plone.app import textfield
from plone.autoform import directives as form
from plone.formwidget.masterselect import MasterSelectBoolField
from plone.formwidget.multifile import MultiFileFieldWidget
from plone.namedfile import field
from plone.supermodel import model

from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.browser.checkbox import SingleCheckBoxFieldWidget

from zope import schema
from zope.interface import implements

import zope


# Applicant's DataGridField schema #

class IApplicantsRowSchema(zope.interface.Interface):
    """
    Schema for DataGridField widget's row of field 'applicants'
    """
    firstname = schema.TextLine(
        title=_(u'Firstname'),
        required=False,
    )

    name = schema.TextLine(
        title=_(u'Name'),
        required=False,
    )


# Parcels DataGridField schema #

class IParcelRowSchema(zope.interface.Interface):
    """
    Schema for DataGridField widget's row of field 'parcels'
    """
    locality = schema.Choice(
        title=_(u'Locality'),
        vocabulary='imio.urbdial.notarydivision.Localities',
        required=False,
    )

    division = schema.TextLine(
        title=_(u'Division'),
        required=False,
    )

    section = schema.TextLine(
        title=_(u'Section'),
        required=False,
    )

    radical = schema.TextLine(
        title=_(u'Radical'),
        required=False,
    )

    bis = schema.TextLine(
        title=_(u'Bis'),
        required=False,
    )

    exposant = schema.TextLine(
        title=_(u'Exposant'),
        required=False,
    )

    power = schema.TextLine(
        title=_(u'Power'),
        required=False,
    )


# NotaryDivision schema #

class IBaseNotaryDivision(model.Schema, INotaryDivisionElement):
    """
    NotaryDivision base dexterity schema
    """

    form.omitted('exclude_from_nav')
    exclude_from_nav = schema.Bool(
        title=_(u'Exclude from navigation'),
        default=True,
    )

    model.fieldset(
        'general',
        label=_(u"General informations"),
        fields=['reference', 'applicants', 'local_dgo4', 'local_township']
    )

    reference = schema.TextLine(
        title=_(u'Reference'),
        required=False,
    )

    form.widget('applicants', DataGridFieldFactory)
    applicants = schema.List(
        title=_(u'Applicants'),
        required=False,
        value_type=DictRow(
            schema=IApplicantsRowSchema,
            required=False
        ),
    )

    local_dgo4 = schema.Set(
        title=_(u'Local DGO4'),
        value_type=schema.Choice(
            vocabulary='imio.urbdial.notarydivision.dgo4s'
        ),
        default=set([TEST_FD_LOCALGROUP]),
        required=False,
    )

    local_township = schema.Set(
        title=_(u'Local township'),
        value_type=schema.Choice(
            vocabulary='imio.urbdial.notarydivision.townships'
        ),
        default=set([TEST_TOWNSHIP_LOCALGROUP]),
        required=False,
    )

    model.fieldset(
        'estate',
        label=_(u"Estate"),
        fields=[
            'street', 'street_number', 'parcels', 'surface', 'actual_use',
            'undivided', 'specific_rights', 'created_parcellings', 'entrusting'
        ]
    )

    street = schema.TextLine(
        title=_(u'Street'),
        required=False,
    )

    street_number = schema.TextLine(
        title=_(u'Street number'),
        required=False,
    )

    form.widget('parcels', ParcelDataGridFieldFactory)
    parcels = schema.List(
        title=_(u'Parcels'),
        required=False,
        value_type=DictRow(
            schema=IParcelRowSchema,
            required=False
        ),
    )

    surface = schema.TextLine(
        title=_(u'Surface'),
        required=False,
    )

    actual_use = schema.Text(
        title=_(u'Estate actual use'),
        required=False,
    )

    undivided = MasterSelectBoolField(
        title=_(u'Case of undivided parcel'),
        required=False,
        slave_fields=(
            {
                'masterID': 'form-widgets-undivided-0',
                'name': 'specific_rights',
                'action': 'show',
                'hide_values': 1,
            },
        ),
    )

    specific_rights = schema.Text(
        required=False,
    )

    created_parcellings = schema.Int(
        title=_(u'Number of created parcellings'),
        required=False,
    )

    form.widget('entrusting', SingleCheckBoxFieldWidget)
    entrusting = schema.Bool(
        title=_(u'Entrusting'),
        required=True,
    )


class BaseNotaryDivision(UrbdialContainer):
    """
    NotaryDivision dexterity class
    """
    implements(IBaseNotaryDivision)

    __ac_local_roles_block__ = True

    def is_in_draft(self):
        return self.get_state() == 'In preparation'

    def get_notification_date(self):
        history = self.workflow_history.values()[0]
        for action in history:
            if action.get('action') == 'Notify':
                return action.get('time')

    def is_passed(self):
        return self.get_state() == 'Passed'

    def get_passed_date(self):
        passed_date = DateTime(self.get_comment_of_state('Passed'))
        return passed_date

    def get_objects(self, state=None, portal_type='', provides=None):
        catalog = api.portal.get_tool('portal_catalog')

        query = {'object_provides': provides.__identifier__}
        if state:
            query['review_state'] = state
        if portal_type:
            query['portal_type'] = portal_type

        brains = catalog(
            path={'query': '/'.join(self.getPhysicalPath())},
            **query
        )
        objects = [brain.getObject() for brain in brains]

        return objects

    def get_comments(self, state=None, portal_type='', provides=IComment):
        """
        Query all comments of the current NotaryDivision.
        """
        comments = self.get_objects(state, portal_type, provides)
        return comments

    def get_parcels(self, state=None, portal_type='', provides=IParcel):
        """
        Query all parcels of the current NotaryDivision.
        """
        parcels = self.get_objects(state, portal_type, provides)
        return parcels


class INotaryDivision(IBaseNotaryDivision):
    """
    NotaryDivision (article 90) dexterity schema
    """

    model.fieldset(
        'article_90',
        label=_(u"Article 90"),
        fields=['article_90', 'article90_detail']
    )

    form.widget('article_90', CheckBoxFieldWidget)
    article_90 = schema.Set(
        title=_(u'Article 90 reasons'),
        value_type=schema.Choice(
            vocabulary='imio.urbdial.notarydivision.Article90Reasons',
        ),
        required=False,
    )

    article90_detail = textfield.RichText(
        title=_(u'Article 90 exceptions detail'),
        required=False,
    )

    model.fieldset(
        'plan',
        label=_(u"Plan"),
        fields=['plan_reference', 'plan_date', 'geometrician', 'plan_files']
    )

    plan_reference = schema.TextLine(
        title=_(u'Plan reference'),
        required=False,
    )

    plan_date = schema.Date(
        title=_(u'Plan date'),
        required=False,
    )

    geometrician = schema.Text(
        title=_(u'Geometrician'),
        required=False,
    )

    form.widget('plan_files', MultiFileFieldWidget)
    plan_files = schema.List(
        title=_(u'Plans files'),
        description=_(u'Other plans must be attached in the «other files» tab.'),
        value_type=field.NamedBlobFile(),
        required=False,
    )

    model.fieldset(
        'annex',
        label=_(u"Annex"),
        fields=['annex_files']
    )

    form.widget('annex_files', MultiFileFieldWidget)
    annex_files = schema.List(
        title=_(u'Annex files'),
        value_type=field.NamedBlobFile(),
        required=False,
    )


class NotaryDivision(BaseNotaryDivision):
    """
    NotaryDivision dexterity class
    """
    implements(INotaryDivision)


class IOtherNotaryDivision(IBaseNotaryDivision):
    """
    NotaryDivision (other reason) dexterity schema
    """

    model.fieldset(
        'otherdivision',
        label=_(u"Reasons"),
        fields=['otherdivision_reason']
    )

    otherdivision_reason = textfield.RichText(
        title=_(u'Other division reason'),
        required=False,
    )

    model.fieldset(
        'plan',
        label=_(u"Plan"),
        fields=['plan_reference', 'plan_date', 'geometrician', 'plan_files']
    )

    plan_reference = schema.TextLine(
        title=_(u'Plan reference'),
        required=False,
    )

    plan_date = schema.Date(
        title=_(u'Plan date'),
        required=False,
    )

    geometrician = schema.Text(
        title=_(u'Geometrician'),
        required=False,
    )

    form.widget('plan_files', MultiFileFieldWidget)
    plan_files = schema.List(
        title=_(u'Plans files'),
        description=_(u'Other plans must be attached in the «other files» tab.'),
        value_type=field.NamedBlobFile(),
        required=False,
    )

    model.fieldset(
        'annex',
        label=_(u"Annex"),
        fields=['annex_files']
    )

    form.widget('annex_files', MultiFileFieldWidget)
    annex_files = schema.List(
        title=_(u'Annex files'),
        value_type=field.NamedBlobFile(),
        required=False,
    )


class OtherNotaryDivision(BaseNotaryDivision):
    """
    NotaryDivision dexterity class
    """
    implements(IOtherNotaryDivision)
