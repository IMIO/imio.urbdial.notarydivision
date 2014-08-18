# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.workflows.state_roles_mapping import UrbdialWorkflowStateRolesMapping


class StateRolesMapping(UrbdialWorkflowStateRolesMapping):
    """ """

    mapping = {
        'Draft': {
            'get_notary_office': ('Parcel Manager',),
        },

        'Published': {
            'notaries': ('Parcel Reader',),
            'dgo4': ('Parcel Reader',),
            'get_local_township': ('Parcel Reader',),
        },
    }
