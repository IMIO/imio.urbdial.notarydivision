# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.workflows.state_roles_mapping import UrbdialWorkflowStateRolesMapping
from imio.urbdial.notarydivision.content.comment import IFDObservation
from imio.urbdial.notarydivision.content.comment import ITownshipObservation


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
                'get_dgo4_observation_creator_role'
            ),
            'get_local_township': (
                'Precision Reader',
                'get_township_observation_creator_role'
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

    def get_dgo4_observation_creator_role(self):
        return self.get_observation_creator_role(
            interface=IFDObservation,
            creation_role='FD Observation Creator'
        )

    def get_township_observation_creator_role(self):
        return self.get_observation_creator_role(
            interface=ITownshipObservation,
            creation_role='Township Observation Creator'
        )

    def get_observation_creator_role(self, interface, creation_role):
        """
        We can create new observations only if theres no draft observations on
        the notarydivision.
        """
        notarydivision = self.obj.get_notarydivision()

        draft_observations = notarydivision.get_comments(interface=interface, state='Draft')
        if draft_observations:
            return ()
        return (creation_role,)
