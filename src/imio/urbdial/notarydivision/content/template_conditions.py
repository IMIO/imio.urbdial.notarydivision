# -*- coding: utf-8 -*-

from collective.documentgenerator.content.condition import PODTemplateCondition

from imio.urbdial.notarydivision.content.comment import IFDObservation
from imio.urbdial.notarydivision.content.comment import ITownshipObservation

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
        return not notarydivision.is_in_draft()


class PassedDocumentCondition(NotaryDocumentsCondition):
    """
    Conditions to generate the document 'Act passed':
    - The notary division should be in state 'Passed'.
    """

    def condition(self):
        notarydivision = self.context
        return notarydivision.is_passed()


class PrecisionFDDocumentCondition(NotificationDocumentCondition):
    """
    Conditions to generate the document 'Precision (FD)':
    - The precision object should be an anwser of a comment done by a FD.
    - The precision object should be at least in state 'published'.
    """

    def condition(self):
        precision = self.context
        # Precision should at least be in state 'published'.
        if precision.is_in_draft():
            return False
        # Precisison should be an answer to an FD Observation.
        if not IFDObservation.providedBy(precision.aq_parent):
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
        if precision.is_in_draft():
            return False
        # Precisison should be an answer to a Township Observation.
        if not ITownshipObservation.providedBy(precision.aq_parent):
            return False
        return True
