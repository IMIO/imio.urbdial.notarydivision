# -*- coding: utf-8 -*-

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow

from imio.urbdial.notarydivision import _
from imio.urbdial.notarydivision.browser.estate_datagridfield import estate_DataGridFieldFactory
from imio.urbdial.notarydivision.browser.field import DataGridBool
from imio.urbdial.notarydivision.content.interfaces import INotaryDivisionElement

from plone import api
from plone.app import textfield
from plone.autoform import directives as form
from plone.dexterity.content import Container
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


# Initial estate's DataGridField schema #

class IInitialEstateRowSchema(zope.interface.Interface):
    """
    Schema for DataGridField widget's row of field 'initial_estate'
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

    surface = schema.TextLine(
        title=_(u'Surface'),
        required=False,
    )

    specific_rights = schema.Text(
        title=_(u'Specific rights'),
        required=False,
    )


# Created estate's DataGridField schema #

class ICreatedEstateRowSchema(zope.interface.Interface):
    """
    Schema for DataGridField widget's row of field 'created_estate'
    We fully duplicate the schema of IInitialEstateRowSchema rather than
    inheriting it because fields reordering is likely impossible to be done
    in a clean way.
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

    surface = schema.TextLine(
        title=_(u'Surface'),
        required=False,
    )

    surface_accuracy = schema.Choice(
        title=_(u'Surface accuracy'),
        vocabulary='imio.urbdial.notarydivision.SurfaceAccuracies',
        required=False,
    )

    built = DataGridBool(
        title=_(u'Built'),
        required=False,
    )

    deed_type = schema.Choice(
        title=_(u'Deed type'),
        vocabulary='imio.urbdial.notarydivision.DeedTypes',
        required=False,
    )

    destination = schema.Text(
        title=_(u'Parcel destination'),
        required=False,
    )

    specific_rights = schema.Text(
        title=_(u'Specific rights'),
        required=False,
    )


# NotaryDivision schema #

class INotaryDivision(model.Schema, INotaryDivisionElement):
    """
    NotaryDivision dexterity schema
    """

    form.omitted('exclude_from_nav')
    exclude_from_nav = schema.Bool(
        title=_(u'Exclude from navigation'),
        default=True,
    )

    model.fieldset(
        'general',
        label=_(u"General informations"),
        fields=['reference', 'applicants']
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

    model.fieldset(
        'estate',
        label=_(u"Estate"),
        fields=['actual_use', 'initial_estate', 'created_estate', 'entrusting']
    )

    actual_use = textfield.RichText(
        title=_(u'Estate actual use'),
        required=False,
    )

    form.widget('initial_estate', estate_DataGridFieldFactory)
    initial_estate = schema.List(
        title=_(u'Initial estate'),
        required=False,
        value_type=DictRow(
            schema=IInitialEstateRowSchema,
            required=False
        ),
    )

    form.widget('created_estate', estate_DataGridFieldFactory)
    created_estate = schema.List(
        title=_(u'Created estate'),
        required=False,
        value_type=DictRow(
            schema=ICreatedEstateRowSchema,
            required=False
        ),
    )

    form.widget('entrusting', SingleCheckBoxFieldWidget)
    entrusting = schema.Bool(
        title=_(u'Entrusting'),
        required=True,
    )

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


class NotaryDivision(Container):
    """
    NotaryDivision dexterity class
    """
    implements(INotaryDivision)

    __ac_local_roles_block__ = True

    def get_notification_date(self):
        history = self.workflow_history.values()[0]
        for action in history:
            if action.get('action') == 'Notify':
                return action.get('time')

    def is_passed(self):
        is_passed = api.content.get_state(self) == 'Passed'
        return is_passed

    def get_passed_date(self):
        history = self.workflow_history.values()[0]
        for action in history:
            if action.get('action') == 'Pass':
                return action.get('time')
