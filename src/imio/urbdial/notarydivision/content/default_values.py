# -*- coding: utf-8 -*-


class AutoIncrementDefaultValue(object):
    """
    """

    def __init__(self, context, request, form, field, widget):
        self.context = context
        self.form = form

    def get(self):
        type_interface = self.form.schema
        default_number = get_parcel_default_number(self.context, type_interface)
        return default_number


def get_parcel_default_number(context, type_interface):
    """
    Compute lowest available default number for a parcel type.
    """

    parcels = context.get_parcels(interface=type_interface)
    existing_numbers = sorted(set([p.number for p in parcels if p.number]))
    default_number = 1

    for number in existing_numbers:
        if default_number < number:
            return default_number
        else:
            default_number += 1

    return default_number
