# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from imio.urbdial.notarydivision.interfaces import IAvailableDocumentsForGeneration
from imio.urbdial.notarydivision.utils import get_pod_templates_folder

from zope.component import queryMultiAdapter
from zope.interface import implements


class DocumentsActionView(BrowserView):
    """
    """

    def __call__(self):
        return ViewPageTemplateFile("templates/documents_action.pt")(self)

    def get_documents(self):
        document_finder = queryMultiAdapter(
            (self.context, self.request),
            IAvailableDocumentsForGeneration,
        )
        if not document_finder:
            return []
        else:
            return document_finder.get_available_templates()

    def get_generation_link(self, document):
        base_url = self.context.absolute_url()
        call = 'document-generation'
        link = '{base_url}/{call}?doc_uid={uid}&output_format=pdf'.format(
            base_url=base_url,
            call=call,
            uid=document.UID(),
        )
        return link


class AvailableDocumentsForGeneration(object):
    """
    Adapts a context and a request and returns a list of PODTemplate UIDs
    """
    implements(IAvailableDocumentsForGeneration)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return self.get_available_templates()

    def get_available_templates(self):
        """
        Filter the list of PODTemplate on their TAL condition.
        """
        pod_templates = self.get_pod_templates()
        TAL_context = self.get_TAL_context()
        available_pod_templates = []
        for pod_template in pod_templates:
            if pod_template.can_be_generated(self.context, TAL_context):
                available_pod_templates.append(pod_template)
        return available_pod_templates

    def get_TAL_context(self):
        """
        Return a dict used as context to evaluate the PODTemplate TAL expression.
        """
        TAL_context = {
            'context': self.context,
            'here': self.context,
            'object': self.context,
            'request': self.request,
        }
        return TAL_context

    def get_pod_templates(self):
        """
        To override.
        Should return a list of PODTemplates.
        """


class DocumentsOfNotaryDivision(AvailableDocumentsForGeneration):
    """
    Documents available for NotaryDivision content type.
    """

    def get_pod_templates(self):
        templates_folder = get_pod_templates_folder()
        pod_templates = [
            getattr(templates_folder, 'notification'),
            getattr(templates_folder, 'information-acte-passe'),
        ]
        return pod_templates


class DocumentsOfPrecision(AvailableDocumentsForGeneration):
    """
    Documents available for NotaryDivision content type.
    """

    def get_pod_templates(self):
        templates_folder = get_pod_templates_folder()
        pod_templates = [
            getattr(templates_folder, 'precision'),
        ]
        return pod_templates
