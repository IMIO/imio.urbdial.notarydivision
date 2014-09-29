# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision import _
from imio.urbdial.notarydivision.content.base import UrbdialItem
from imio.urbdial.notarydivision.content.interfaces import INotaryDivisionElement

from plone.autoform import directives as form
from plone.formwidget.masterselect import MasterSelectBoolField
from plone.formwidget.masterselect import MasterSelectField
from plone.formwidget.masterselect import MasterSelectRadioField
from plone.supermodel import model

from zope import schema
from zope.interface import implements


class IParcelling(model.Schema, INotaryDivisionElement):
    """
    Schema of Parcelling
    """

    number = schema.Int(
        title=_(u'Number'),
        required=False,
    )

    localisation = schema.Text(
        title=_(u'Parcelling localisation'),
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

    form.order_before(surface='surface_accuracy')

    surface_accuracy = schema.Choice(
        vocabulary='imio.urbdial.notarydivision.SurfaceAccuracies',
    )

    road_distance = schema.TextLine(
        title=_(u'Road distance'),
        required=False,
    )

    destination = schema.Text(
        title=_(u'Parcelling destination'),
        required=False,
    )

    ceded_parcelling = MasterSelectRadioField(
        title=_(u'Ceded'),
        default=True,
        vocabulary='imio.urbdial.notarydivision.CededVocabulary',
        slave_fields=(
            {
                'masterID': 'form-widgets-ceded_parcelling-1',
                'name': 'deed_type',
                'action': 'hide',
                'hide_values': 'no',
                'siblings': True,
            },
            {
                'masterID': 'form-widgets-ceded_parcelling-1',
                'name': 'other_deed_type',
                'action': 'hide',
                'hide_values': 'no',
                'siblings': True,
            },
            {
                'masterID': 'form-widgets-ceded_parcelling-0',
                'name': 'deed_type',
                'action': 'show',
                'hide_values': 'yes',
                'siblings': True,
            },
        ),
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
