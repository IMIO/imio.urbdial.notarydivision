# -*- coding: utf-8 -*-

from collective.documentgenerator.content.condition import PODTemplateCondition

from plone import api


class NotaryDocumentsCondition(PODTemplateCondition):
    """
    Base class for document conditions of notaries.
    Document generation should only be available for notaries.
    """

    def evaluate(self):
        if not self.current_user_is_notary():
            return False

        return self.condition()

    def condition(self):
        """
        To implements.
        """

    def current_user_is_notary(self):
        user_name = api.user.get_current().getUserName()
        notary_group = api.group.get('notaries')
        user_groups = api.group.get_groups(user_name)
        is_notary = notary_group in user_groups
        return is_notary


class NotificationDocumentCondition(NotaryDocumentsCondition):
    """
    Conditions to generate the document 'Notification':
    - The notary division should be at least in state 'in investigation'.
    """

    def condition(self):
        notarydivision = self.context
        # Notarydivision is at least in state 'In preparation'.
        if api.content.get_state(notarydivision) == 'In preparation':
            return False
        return True


class PassedDocumentCondition(NotaryDocumentsCondition):
    """
    Conditions to generate the document 'Act passed':
    - The notary division should be in state 'Passed'.
    """

    def condition(self):
        notarydivision = self.context
        # Notarydivision is in state 'Passed'.
        if api.content.get_state(notarydivision) == 'Passed':
            return True
        return False


class PrecisionFDDocumentCondition(NotificationDocumentCondition):
    """
    Conditions to generate the document 'Precision (FD)':
    - The precision object should be an anwser of a comment done by a FD.
    - The precision object should be at least in state 'published'.
    """

    def condition(self):
        precision = self.context
        # Precision should at least be in state 'published'.
        if api.content.get_state(precision) == 'Draft':
            return False

        container = precision.aq_parent
        # Precision should be an answer to an observation.
        if container.portal_type not in ['Observation', 'InadmissibleFolder', 'PrecisionDemand']:
            return False

        # The answered comment should be written by a FD.
        if not container.is_dgo4_or_township() == 'dgo4':
            return False

        return True


class PrecisionACDocumentCondition(NotificationDocumentCondition):
    """
    Conditions to generate the document 'Precision (AC)':
    - The precision object should be an anwser of a comment done by a towsnhip user.
    - The precision object should be at least in state 'published'.
    """

    def condition(self):
        precision = self.context
        # Precision should at least be in state 'published'.
        if api.content.get_state(precision) == 'Draft':
            return False

        container = precision.aq_parent
        # Precision should be an answer to an observation.
        if container.portal_type not in ['Observation', 'InadmissibleFolder', 'PrecisionDemand']:
            return False

        # The answered comment should be written by a AC.
        if not container.is_dgo4_or_township() == 'townships':
            return False

        return True
