# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.workflows.state_roles_mapping import UrbdialWorkflowStateRolesMapping


class StateRolesMapping(UrbdialWorkflowStateRolesMapping):
    """ """

    mapping = {
        'In preparation': {
            'notary_office': (
                'NotaryDivision Manager',
                'Notification Manager',
            ),
        },

        'In investigation': {
            'notary_office': (
                'Notification Manager',
                'NotaryDivision Reader',
                'Precision Creator',
            ),
            'local_township': (
                'NotaryDivision Reader',
                'Observation Creator',
            ),
            'local_dgo4': (
                'NotaryDivision Reader',
                'Observation Creator',
            ),
            'notaries': ('NotaryDivision Reader',),
            'dgo4': ('NotaryDivision Reader',),
        },

        'Passed': {
            'notaries': ('NotaryDivision Reader',),
            'local_township': ('NotaryDivision Reader',),
            'dgo4': ('NotaryDivision Reader',),
        },

        'Cancelled': {
            'notaries': ('NotaryDivision Reader',),
            'local_township': ('NotaryDivision Reader',),
            'dgo4': ('NotaryDivision Reader',),
        },
    }
