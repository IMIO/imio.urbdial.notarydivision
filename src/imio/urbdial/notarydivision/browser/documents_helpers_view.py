# -*- coding: utf-8 -*-

from Products.Five import BrowserView

from plone import api

from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory


class DocumentGenerationHelperView(BrowserView):
    """
    View containing helper methods for document generation.
    """

    def __init__(self, context, request):
        super(DocumentGenerationHelperView, self).__init__(context, request)
        self.context = context
        self.request = request
        self.notarydivision = context.portal_type == 'NotaryDivision' and context or context.get_notarydivision()

    def date(self, date):
        return date.strftime('%d/%m/%Y')

    def fullname(self, username):
        return api.user.get(username).getProperty('fullname')

    def initial_estate_locality(self):
        voc_factory = queryUtility(IVocabularyFactory, "imio.urbdial.notarydivision.Localities")
        localies_voc = voc_factory(self.notarydivision)

        localities = []
        for row in self.notarydivision.initial_estate:
            locality = localies_voc.getTerm(row['locality']).title
            if locality not in localities:
                localities.append(locality)

        return ', '.join(list(localities))

    def initial_estate_cadastral_ref(self):
        cadastral_references = []
        for row in self.notarydivision.initial_estate:
            cadastral_references.append(self.get_reference_display(row))
        return ', '.join(cadastral_references)

    def get_reference_display(self, line):
        reference_fields = ['division', 'section', 'radical', 'bis', 'exposant', 'power']
        reference = ''
        for name in reference_fields:
            val = line[name]
            if val:
                if name == 'bis':
                    reference = '{ref}/{val}'.format(ref=reference, val=val)
                else:
                    reference = '{ref} {val}'.format(ref=reference, val=val)
        return reference

    def list_attachments(self, comment=None):
        if not comment:
            comment = self.context
        return ', '.join([f.filename for f in comment.files])
