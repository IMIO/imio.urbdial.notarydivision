# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.workflows.state_roles_mapping import UrbdialWorkflowStateRolesMapping


class StateRolesMapping(UrbdialWorkflowStateRolesMapping):
    """ """

    mapping = {
        'Draft': {
            'get_notary_office': ('Precision Manager',),
        },

        'Published': {
            'get_notary_office': (
                'Precision Reader',
                'Precision Creator'
            ),
            'get_local_dgo4': (
                'Precision Reader',
                'Observation Creator'
            ),
            'get_local_township': (
                'Precision Reader',
                'Observation Creator'
            ),
            'dgo4': ('Precision Reader',),
            'notaries': ('Precision Reader',),
        },

        'Frozen': {
            'notaries': ('Precision Reader',),
            'dgo4': ('Precision Reader',),
            'get_local_township': ('Precision Reader',),
        },
    }
