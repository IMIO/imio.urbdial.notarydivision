# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.workflows.state_roles_mapping import WorkflowStateRolesMapping


class StateRolesMapping(WorkflowStateRolesMapping):
    """ """

    mapping = {
        'In preparation': {
            'notaries': (
                'NotaryDivision Manager',
                'Notification Manager',
            ),
        },
        'In investigation': {
            'notaries': (
                'Notification Manager',
                'NotaryDivision Reader',
                'Precision Creator',
            ),
            'townships': (
                'NotaryDivision Reader',
                'Observation Creator',
            ),
            'dgo4': (
                'NotaryDivision Reader',
                'Observation Creator',
            ),
        },
        'Passed': {
            'notaries': (
                'NotaryDivision Reader',
            ),
            'townships': (
                'NotaryDivision Reader',
            ),
            'dgo4': (
                'NotaryDivision Reader',
            ),
        },
        'Cancelled': {
            'notaries': (
                'NotaryDivision Reader',
            ),
            'townships': (
                'NotaryDivision Reader',
            ),
            'dgo4': (
                'NotaryDivision Reader',
            ),
        },
    }
