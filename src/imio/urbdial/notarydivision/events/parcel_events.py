# -*- coding: utf-8 -*-

from plone import api


def handle_z3cform_bug(created_parcel, event):
    """
    z3c.form/dexterity bug: the "save" button of the CreatedParcel add form also trigger
    the save action of the InitialParcel add form. So when a new CreatedParcel is created
    ttw, an undesired InitialParcel is also created. We delete it through this event.
    """
    notarydivision = created_parcel.get_notarydivision()
    initial_parcels = notarydivision.get_parcels(portal_type='InitialParcel')
    initial_parcels = sorted(initial_parcels, key=lambda parcel: parcel.created())

    if initial_parcels:
        last_initial_parcel = initial_parcels[-1]
        # the delta between creation date should be very low
        if created_parcel.created() - last_initial_parcel.created() < 0.0001:
            api.content.delete(last_initial_parcel)
            return created_parcel.REQUEST.response.redirect(created_parcel.absolute_url() + '/view')
