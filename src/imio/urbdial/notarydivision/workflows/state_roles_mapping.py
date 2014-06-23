# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.workflows.interfaces import IWorkflowStateRolesMapping

from zope.interface import implements


class WorkflowStateRolesMapping(object):
    """
    Store mapping between roles and groups for each state of a given workflow.
    This mapping is registered as a named multiadapter adapting  an object and
    its workflow.
    """
    implements(IWorkflowStateRolesMapping)

    mapping = {}

    def __init__(self, obj, workflow):
        self.obj = obj

    def get_group_roles_mapping_of(self, state):
        """
        Return the group/roles mapping of a given state.
        """
        group_roles_mapping = self.mapping.get(state, {})
        generated_mapping = {}

        for group_name, role_names in group_roles_mapping.iteritems():
            group = self.compute_value(group_name)

            roles = []
            for role_name in role_names:
                role = self.compute_value(role_name)
                roles.append(role)

            generated_mapping[group] = roles

        return generated_mapping

    def compute_value(self, value_name):
        """
        Values in the mapping can be either the value to return or a method name to
        call to dynamically compute the value.
        """
        if hasattr(self, value_name):
            value_computation_method = getattr(self, value_name)
            value = value_computation_method()
        else:
            value = value_name
        return value


class UrbdialWorkflowStateRolesMapping(WorkflowStateRolesMapping):
    """
    """

    def notary_office(self):
        """
        """
        return 'notaries'

    def local_dgo4(self):
        """
        """
        return 'dgo4_namur'

    def local_township(self):
        """
        """
        return 'ac_sambreville'
