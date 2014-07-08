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
        templates_finder = queryMultiAdapter(
            (self.context, self.request),
            IAvailableDocumentsForGeneration,
        )
        if not templates_finder:
            return []
        else:
            return templates_finder.get_available_templates()

    def get_generation_link(self, document):
        base_url = self.context.absolute_url()
        output_format = 'pdf'
        call = 'document-generation'
        link = '{base_url}/{call}?doc_uid={uid}&output_format={mimetype}'.format(
            base_url=base_url,
            call=call,
            uid=document.UID(),
            mimetype=output_format,
        )
        return link


class AvailableDocumentsForGeneration(object):
    """
    Adapts a context and a request and returns a list of PODTemplates.
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
        available_templates = [t for t in pod_templates if t.can_be_generated(self.context)]
        return available_templates

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
            getattr(templates_folder, 'notification-ac'),
            getattr(templates_folder, 'notification-fd'),
            getattr(templates_folder, 'acte-passe-ac'),
            getattr(templates_folder, 'acte-passe-fd'),
        ]
        return pod_templates


class DocumentsOfPrecision(AvailableDocumentsForGeneration):
    """
    Documents available for NotaryDivision content type.
    """

    def get_pod_templates(self):
        templates_folder = get_pod_templates_folder()
        pod_templates = [
            getattr(templates_folder, 'precision-ac'),
            getattr(templates_folder, 'precision-fd'),
        ]
        return pod_templates
