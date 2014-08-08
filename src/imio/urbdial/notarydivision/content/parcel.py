# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision import _
from imio.urbdial.notarydivision.content.base import UrbdialItem

from plone.formwidget.masterselect import MasterSelectBoolField

from zope import schema
from zope.interface import implements

import zope


class IParcel(zope.interface.Interface):
    """
    Schema of Parcel
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


class IInitialParcel(IParcel):
    """
    Schema of InitialParcel
    """

    actual_use = schema.Text(
        title=_(u'Estate actual use'),
        required=False,
    )

    surface = schema.TextLine(
        title=_(u'Surface'),
        required=False,
    )

    # Add a '_a' at the end of the field so it can be distinguished from
    # undivided_b to avoid javascript issues with the boolean master select
    # widget.
    undivided_a = MasterSelectBoolField(
        title=_(u'Case of undivided parcel'),
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


class InitialParcel(UrbdialItem):
    """
    InitialParcel dexterity class
    """
    implements(IInitialParcel)

    __ac_local_roles_block__ = True


class ICreatedParcel(IParcel):
    """
    Schema of CreatedParcel
    """

    destination = schema.Text(
        title=_(u'Parcel destination'),
        required=False,
    )

    surface = schema.TextLine(
        title=_(u'Surface'),
        required=False,
    )

    surface_accuracy = schema.Choice(
        vocabulary='imio.urbdial.notarydivision.SurfaceAccuracies',
        required=False,
    )

    deed_type = schema.Choice(
        title=_(u'Deed type'),
        vocabulary='imio.urbdial.notarydivision.DeedTypes',
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


class CreatedParcel(InitialParcel):
    """
    CreatedParcel dexterity class
    """
    implements(ICreatedParcel)
