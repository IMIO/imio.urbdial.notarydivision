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
                'get_local_dgo4_observation_creator_role'
            ),
            'get_local_township': (
                'Precision Reader',
                'get_local_township_observation_creator_role'
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

    def get_local_dgo4_observation_creator_role(self):
        """
        'Observation Creator' role is only available for local_dgo4 if there is no draft
        Observation created by local_dgo4.
        """
        return self.get_observation_creator_role_for_group('dgo4')

    def get_local_township_observation_creator_role(self):
        """
        'Observation Creator' role is only available for local_township if there is no draft
        Observation created by local_township.
        """
        return self.get_observation_creator_role_for_group('townships')

    def get_observation_creator_role_for_group(self, local_group):
        notarydivision = self.obj.get_notarydivision()

        draft_observations = notarydivision.get_comments(portal_type='Observation', state='Draft')

        for observation in draft_observations:
            if observation.is_dgo4_or_township() == local_group:
                return ()
        return ('Observation Creator',)
