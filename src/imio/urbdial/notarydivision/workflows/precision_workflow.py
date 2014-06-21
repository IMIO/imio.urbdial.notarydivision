# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.workflows.state_roles_mapping import WorkflowStateRolesMapping


class StateRolesMapping(WorkflowStateRolesMapping):
    """ """

    mapping = {
        'Draft': {
            'notaries': ('Precision Manager',),
        },
        'Published': {
            'notaries': ('Precision Reader', 'Precision Creator'),
            'dgo4': ('Precision Reader', 'Observation Creator'),
            'townships': ('Precision Reader', 'Observation Creator'),
        },
        'Frozen': {
            'notaries': ('Precision Reader',),
            'dgo4': ('Precision Reader',),
            'townships': ('Precision Reader',),
        },
    }
