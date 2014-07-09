# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.workflows.interfaces import IWorkflowStateRolesMapping
from imio.urbdial.notarydivision.utils import get_notarydivision

from plone import api

from zope.interface import implements


class GroupNotFoundError(Exception):
    """ """


class RoleNotFoundError(Exception):
    """ """


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
            groups = self.compute_group_value(group_name)

            roles = []
            for role in role_names:
                roles.extend(self.compute_role_value(role))
            roles = list(set(roles))

            for group in groups:
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
            value = [value_name]
        return value

    def compute_group_value(self, group_name):
        group_values = self.compute_value(group_name)
        for group_value in group_values:
            if not api.group.get(group_value):
                if hasattr(self, group_name):
                    msg = "Group '{}' computed by '{}' method does not exist.".format(group_value, group_name)
                else:
                    msg = "'{}' is neither an existing group nor a method on mapping object {}.".format(
                        group_name,
                        self,
                    )
                raise GroupNotFoundError(msg)
        return group_values

    def compute_role_value(self, role_name):
        role_values = self.compute_value(role_name)

        portal = api.portal.getSite()
        portal_roles = portal.acl_users.portal_role_manager
        registered_roles = portal_roles.listRoleIds()
        for role_value in role_values:
            if role_value not in registered_roles:
                if hasattr(self, role_name):
                    msg = "Role '{}' computed by '{}' method does not exist.".format(role_value, role_name)
                else:
                    msg = "'{}' is neither an existing role nor a method on mapping object {}.".format(
                        role_name,
                        self,
                    )
                raise RoleNotFoundError(msg)
        return role_values


class UrbdialWorkflowStateRolesMapping(WorkflowStateRolesMapping):
    """
    Helper class to store urbdial workflows local roles/groups mapping with methods
    to dynamically compute groups such as local_dgo4 or local_township.
    """

    def get_notary_office(self):
        return ['notaries']

    def get_local_dgo4(self):
        notarydivision = get_notarydivision(self.obj)
        return notarydivision.local_dgo4

    def get_local_township(self):
        notarydivision = get_notarydivision(self.obj)
        return notarydivision.local_township
