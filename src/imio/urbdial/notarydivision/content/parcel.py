# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision import _
from imio.urbdial.notarydivision.content.base import UrbdialItem

from zope import schema
from zope.interface import implements

import zope


class IInitialParcel(zope.interface.Interface):
    """
    Schema of InitialParcel
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

    undivided = schema.Bool(
        title=_(u'Case of undivided parcel'),
    )

    specific_rights = schema.Text(
        title=_(u'Specific rights'),
        required=False,
    )

    surface = schema.TextLine(
        title=_(u'Surface'),
        required=False,
    )


class InitialParcel(UrbdialItem):
    """
    InitialParcel dexterity class
    """
    implements(IInitialParcel)

    __ac_local_roles_block__ = True


class ICreatedParcel(IInitialParcel):
    """
    Schema of CreatedParcel
    """

    surface_accuracy = schema.Choice(
        title=_(u'Surface accuracy'),
        vocabulary='imio.urbdial.notarydivision.SurfaceAccuracies',
        required=False,
    )

    built = schema.Bool(
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


class CreatedParcel(InitialParcel):
    """
    CreatedParcel dexterity class
    """
    implements(ICreatedParcel)
