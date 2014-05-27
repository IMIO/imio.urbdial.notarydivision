# -*- coding: utf-8 -*-

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow

from imio.urbdial.notarydivision import _
from imio.urbdial.notarydivision.browser.estate_datagridfield import estate_DataGridFieldFactory
from imio.urbdial.notarydivision.content.interfaces import IDataGridBool

from plone.autoform import directives as form
from plone.dexterity.content import Container
from plone.supermodel import model

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

class DataGridBool(schema.Bool):
    """ """
    implements(IDataGridBool)


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

class INotaryDivision(model.Schema):
    """
    NotaryDivision dexterity schema
    """

    form.omitted('exclude_from_nav')
    exclude_from_nav = schema.Bool(
        title=_(u'Exclude from navigation'),
        default=True,
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

    actual_use = schema.Text(
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


class NotaryDivision(Container):
    """
    NotaryDivision dexterity class
    """
    implements(INotaryDivision)

    __ac_local_roles_block__ = True
