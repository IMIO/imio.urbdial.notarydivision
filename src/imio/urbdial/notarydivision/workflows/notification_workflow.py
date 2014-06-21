# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.workflows.state_roles_mapping import WorkflowStateRolesMapping


class StateRolesMapping(WorkflowStateRolesMapping):
    """ """

    mapping = {
        'In preparation': {
            'notaries': ('NotaryDivision Manager',),
        },
        'In investigation': {
            'townships': (
                'NotaryDivision Reader',
                'Observation Creator',
            ),
            'dgo4': (
                'NotaryDivision Reader',
                'Observation Creator',
            ),
            'notaries': (
                'NotaryDivision Reader',
                'Precision Creator',
            ),
        },
        'Passed': {
            'townships': (
                'NotaryDivision Reader',
            ),
            'dgo4': (
                'NotaryDivision Reader',
            ),
            'notaries': (
                'NotaryDivision Reader',
            ),
        },
        'Cancelled': {
            'townships': (
                'NotaryDivision Reader',
            ),
            'dgo4': (
                'NotaryDivision Reader',
            ),
            'notaries': (
                'NotaryDivision Reader',
            ),
        },
    }
