# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.workflows.state_roles_mapping import WorkflowStateRolesMapping


class StateRolesMapping(WorkflowStateRolesMapping):
    """ """

    mapping = {
        'Draft': {
            'dgo4': ('Observation Manager',),
        },
        'Published': {
            'dgo4': ('Observation Reader', 'Observation Creator'),
            'townships': ('Observation Reader', 'Observation Creator'),
            'notaries': ('Observation Reader', 'Precision Creator'),
        },
        'Frozen': {
            'dgo4': ('Observation Reader',),
            'townships': ('Observation Reader',),
            'notaries': ('Observation Reader',),
        },
    }
