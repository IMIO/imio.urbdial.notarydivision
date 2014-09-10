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


class IParcelling(model.Schema, INotaryDivisionElement):
    """
    Schema of Parcelling
    """

    number = fields.AutoIncrementInt(
        title=_(u'Number'),
        required=False,
    )

    street = schema.TextLine(
        title=_(u'Street'),
        required=False,
    )

    street_number = schema.TextLine(
        title=_(u'Street number'),
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

    surface = schema.TextLine(
        title=_(u'Surface'),
        required=False,
    )


class Parcelling(UrbdialItem):
    """
    Parcelling base class
    """

    __ac_local_roles_block__ = True

    def get_notarydivision(self):
        return self.aq_parent


class ICreatedParcelling(IParcelling):
    """
    Schema of CreatedParcelling
    """

    destination = schema.Text(
        title=_(u'Parcelling destination'),
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

    undivided = MasterSelectBoolField(
        title=_(u'Case of undivided parcelling'),
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


class CreatedParcelling(Parcelling):
    """
    CreatedParcelling dexterity class
    """
    implements(ICreatedParcelling)
