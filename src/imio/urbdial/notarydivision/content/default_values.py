# -*- coding: utf-8 -*-


class AutoIncrementDefaultValue(object):
    """
    z3c.form default value adapter for AutoIncrementInt field.
    """

    def __init__(self, context, request, form, field, widget):
        self.context = context
        self.form = form
        self.field = field

    def get(self):
        """
        Return the first available value amongst objects of the same type
        in the container.
        """
        existing_values = self.get_existing_values()

        default_value = 1

        for value in existing_values:
            if default_value < value:
                return default_value
            else:
                default_value += 1

        return default_value

    def get_existing_values(self):
        """
        Return field values of other objects of the same type in the container.
        """
        type_interface = self.form.schema
        context = self.context
        fieldname = self.field.getName()
        objects = context.get_objects(interface=type_interface)

        existing_values = []
        for obj in objects:
            val = getattr(obj, fieldname)
            if val:
                existing_values.append(val)

        existing_values = sorted(set(existing_values))

        return existing_values
