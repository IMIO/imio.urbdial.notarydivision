# -*- coding: utf-8 -*-

from zope.interface import Interface


class IWorkflowStateRolesMapping(Interface):
    """Interface for WorkflowStateRolesMapping."""

    def get_group_roles_mapping_of(state):
        """Returns local roles mapping of a given state."""


class IObservationWorkflow(Interface):
    """Marker interface for Observation workflow."""


class IPrecisionWorkflow(Interface):
    """Marker interface for Precision workflow."""


class INotificationWorkflow(Interface):
    """Marker interface for NotaryDivision workflow."""
