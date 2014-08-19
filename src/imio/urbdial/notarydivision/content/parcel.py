# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision import _
from imio.urbdial.notarydivision.content import fields
from imio.urbdial.notarydivision.content.base import UrbdialItem
from imio.urbdial.notarydivision.content.interfaces import INotaryDivisionElement

from plone.autoform import directives as form
from plone.formwidget.masterselect import MasterSelectBoolField
from plone.formwidget.masterselect import MasterSelectField
from plone.supermodel import model

from zope import schema
from zope.interface import implements


class IParcel(model.Schema, INotaryDivisionElement):
    """
    Schema of Parcel
    """

    number = fields.AutoIncrementInt(
        title=_(u'Number'),
        required=False,
    )

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

    surface = schema.Int(
        title=_(u'Surface'),
        required=False,
    )


class Parcel(UrbdialItem):
    """
    Parcel base class
    """

    __ac_local_roles_block__ = True

    def get_notarydivision(self):
        return self.aq_parent


class IInitialParcel(IParcel):
    """
    Schema of InitialParcel
    """

    actual_use = schema.Text(
        title=_(u'Estate actual use'),
        required=False,
    )

    form.order_before(surface='undivided_a')

    # Add a '_a' at the end of the field so it can be distinguished from
    # undivided_b to avoid javascript issues with the boolean master select
    # widget.
    undivided_a = MasterSelectBoolField(
        title=_(u'Case of undivided parcel'),
        required=False,
        slave_fields=(
            {
                'masterID': 'form-widgets-undivided_a-0',
                'name': 'specific_rights_a',
                'action': 'show',
                'hide_values': 1,
            },
        ),
    )

    specific_rights_a = schema.Text(
        required=False,
    )


class InitialParcel(Parcel):
    """
    InitialParcel dexterity class
    """
    implements(IInitialParcel)


class ICreatedParcel(IParcel):
    """
    Schema of CreatedParcel
    """

    destination = schema.Text(
        title=_(u'Parcel destination'),
        required=False,
    )

    form.order_before(surface='surface_accuracy')

    surface_accuracy = schema.Choice(
        vocabulary='imio.urbdial.notarydivision.SurfaceAccuracies',
    )

    road_distance = schema.TextLine(
        title=_(u'Road distance'),
        required=False,
    )

    road_distance_accuracy = schema.Choice(
        vocabulary='imio.urbdial.notarydivision.SurfaceAccuracies',
    )

    deed_type = MasterSelectField(
        title=_(u'Deed type'),
        vocabulary='imio.urbdial.notarydivision.DeedTypes',
        slave_fields=(
            {
                'name': 'other_deed_type',
                'action': 'show',
                'hide_values': ('autre',),
                'siblings': True,
            },
        )
    )

    other_deed_type = schema.TextLine(
        title=_(u'Other deed type'),
        required=False,
    )

    built = schema.Bool(
        title=_(u'Built'),
        required=False,
    )

    # Add a '_b' at the end of the field so it can be distinguished from
    # undivided_a to avoid javascript issues with the boolean master select
    # widget.
    undivided_b = MasterSelectBoolField(
        title=_(u'Case of undivided parcel'),
        required=False,
        slave_fields=(
            {
                'masterID': 'form-widgets-undivided_b-0',
                'name': 'specific_rights_b',
                'action': 'show',
                'hide_values': 1,
            },
        ),
    )

    specific_rights_b = schema.Text(
        required=False,
    )


class CreatedParcel(Parcel):
    """
    CreatedParcel dexterity class
    """
    implements(ICreatedParcel)
