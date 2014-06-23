# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.workflows.state_roles_mapping import UrbdialWorkflowStateRolesMapping

from plone import api


class StateRolesMapping(UrbdialWorkflowStateRolesMapping):

    mapping = {
        'Draft': {
            'local_dgo4_or_township': ('Observation Manager',),
        },

        'Published': {
            'local_dgo4': (
                'Observation Reader',
                'Observation Creator'
            ),
            'local_township': (
                'Observation Reader',
                'Observation Creator'
            ),
            'notary_office': (
                'Observation Reader',
                'Precision Creator'
            ),
            'dgo4': ('Observation Reader',),
            'notaries': ('Observation Reader'),
        },

        'Frozen': {
            'dgo4': ('Observation Reader',),
            'local_township': ('Observation Reader',),
            'notaries': ('Observation Reader',),
        },
    }

    def local_dgo4_or_township(self):
        """
        Return the local group of comment's creator (dgo4 or township).
        """
        creator_name = self.obj.creators[0]
        creator_groups = api.group.get_groups(creator_name)

        for group in creator_groups:
            group_id = group.id
            if group_id == self.local_dgo4():
                return self.local_dgo4()
            if group_id == self.local_township():
                return self.local_township()
