# -*- coding: utf-8 -*-

from Products.Five import BrowserView

from imio.urbdial.notarydivision.utils import get_notarydivision

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
        self.notarydivision = get_notarydivision(context)

    def get_vocabulary_of_field(self, field_name='', obj=None):
        if obj is None:
            obj = self.context

        portal_types = api.portal.get_tool('portal_types')
        fti = portal_types.get(obj.portal_type)
        schema = fti.lookupSchema()
        field = schema.get(field_name)
        voc_factory = queryUtility(IVocabularyFactory, field.value_type.vocabularyName)

        vocabulary = voc_factory(obj)
        return vocabulary

    def display_voc_value_of_field(self, field_name='', value='', obj=None):
        if obj is None:
            obj = self.context
        if value is '':
            value = getattr(obj, field_name)

        vocabulary = self.get_vocabulary_of_field(field_name)
        term = vocabulary.getTerm(value)
        return term.title

    def display_voc_values_of_field(self, field_name='', values=[], obj=None):
        if obj is None:
            obj = self.context
        if values == []:
            values = getattr(obj, field_name)

        display_values = [self.display_voc_value_of_field(field_name, val, obj) for val in values]

        return ', '.join(display_values)

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

    def list_applicants(self):
        applicants = ['{} {}'.format(a['firstname'], a['name']) for a in self.context.applicants]

        if not applicants:
            display = ''
        elif len(applicants) == 1:
            display = applicants[0]
        elif len(applicants) == 2:
            display = ' et '.join(applicants[-2:])
        else:
            display_head = ', '.join(applicants[0:-2])
            display_tail = ' et '.join(applicants[-2:])
            display = '{}, {}'.format(display_head, display_tail)

        return display
