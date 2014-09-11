# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.workflows.state_roles_mapping import UrbdialWorkflowStateRolesMapping


class StateRolesMapping(UrbdialWorkflowStateRolesMapping):
    """ """

    mapping = {
        'Draft': {
            'get_notary_office': ('Parcelling Manager',),
        },

        'Published': {
            'notaries': ('Parcelling Reader',),
            'dgo4': ('Parcelling Reader',),
            'get_local_township': ('Parcelling Reader',),
        },
    }
