# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.workflows.interfaces import IWorkflowStateRolesMapping

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
            group = self.compute_group_value(group_name)

            roles = [self.compute_role_value(role) for role in role_names]

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

    def compute_group_value(self, group_name):
        group_value = self.compute_value(group_name)
        if not api.group.get(group_value):
            if hasattr(self, group_name):
                msg = "Group '{}' does not exist.".format(group_value)
            else:
                msg = "'{}' is neither an existing group nor a method on mapping object {}.".format(
                    group_name,
                    self,
                )
            raise GroupNotFoundError(msg)
        return group_value

    def compute_role_value(self, role_name):
        role_value = self.compute_value(role_name)

        portal = api.portal.getSite()
        portal_roles = portal.acl_users.portal_role_manager
        registered_roles = portal_roles.listRoleIds()
        if role_value not in registered_roles:
            if hasattr(self, role_name):
                msg = "Role '{}' does not exist.".format(role_value)
            else:
                msg = "'{}' is neither an existing role nor a method on mapping object {}.".format(
                    role_name,
                    self,
                )
            raise RoleNotFoundError(msg)
        return role_value


class UrbdialWorkflowStateRolesMapping(WorkflowStateRolesMapping):
    """
    """

    def get_notary_office(self):
        """
        """
        return 'notaries'

    def get_local_dgo4(self):
        """
        """
        return 'dgo4_namur'

    def get_local_township(self):
        """
        """
        return 'ac_sambreville'
