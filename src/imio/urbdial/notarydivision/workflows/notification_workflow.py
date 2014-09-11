# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.workflows.state_roles_mapping import UrbdialWorkflowStateRolesMapping


class StateRolesMapping(UrbdialWorkflowStateRolesMapping):
    """ """

    mapping = {
        'In preparation': {
            'get_notary_office': (
                'NotaryDivision Manager',
                'Notification Manager',
                'Parcelling Creator',
            ),
        },

        'In investigation': {
            'get_notary_office': (
                'Notification Manager',
                'NotaryDivision Reader',
                'Precision Creator',
            ),
            'get_local_township': (
                'NotaryDivision Reader',
                'Township Observation Creator',
            ),
            'get_local_dgo4': (
                'NotaryDivision Reader',
                'FD Observation Creator',
            ),
            'notaries': ('NotaryDivision Reader',),
            'dgo4': ('NotaryDivision Reader',),
        },

        'Passed': {
            'notaries': ('NotaryDivision Reader',),
            'get_local_township': ('NotaryDivision Reader',),
            'dgo4': ('NotaryDivision Reader',),
        },

        'Cancelled': {
            'notaries': ('NotaryDivision Reader',),
            'get_local_township': ('NotaryDivision Reader',),
            'dgo4': ('NotaryDivision Reader',),
        },
    }
