# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.content.parcelling import IParcelling

from z3c.form.widget import ComputedWidgetAttribute


def parcelling_default_number(data):
    """
    Return the first available parcelling number.
    """
    divnot = data.context
    parcellings = divnot.get_objects(provides=IParcelling)
    existing_values = set([p.number for p in parcellings])
    default_number = 1

    while default_number in existing_values:
        default_number += 1

    return default_number

ParcellingNumberDefaultValue = ComputedWidgetAttribute(
    parcelling_default_number,
    field=IParcelling['number']
)
