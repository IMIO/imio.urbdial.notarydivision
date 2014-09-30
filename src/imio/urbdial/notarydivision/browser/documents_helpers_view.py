# -*- coding: utf-8 -*-

from Products.Five import BrowserView

from imio.urbdial.notarydivision.utils import aq_notarydivision

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
        self.notarydivision = aq_notarydivision(context)

    def get_vocabulary_of_field(self, field_name='', obj=None):
        if obj is None:
            obj = self.context

        portal_types = api.portal.get_tool('portal_types')
        fti = portal_types.get(obj.portal_type)
        schema = fti.lookupSchema()
        field = schema.get(field_name)
        voc_name = getattr(field, 'vocabularyName', None) or field.value_type.vocabularyName
        voc_factory = queryUtility(IVocabularyFactory, voc_name)

        vocabulary = voc_factory(obj)
        return vocabulary

    def display_voc_value_of_field(self, field_name, value='', obj=None):
        if obj is None:
            obj = self.context
        if value == '':
            value = getattr(obj, field_name)

        vocabulary = self.get_vocabulary_of_field(field_name, obj)
        term = vocabulary.getTerm(value)
        return term.title

    def display_values(self, field_name, values=[], obj=None):
        if obj is None:
            obj = self.context
        if values == []:
            values = getattr(obj, field_name)

        display_values = [self.display_voc_value_of_field(field_name, val, obj) for val in values]

        return ', '.join(display_values)

    def display_value(self, field_name, value='', obj=None):
        if value == '':
            value = getattr(obj, field_name)
        return self.display_voc_value_of_field(field_name, value, obj)

    def date(self, date):
        return date.strftime('%d/%m/%Y')

    def fullname(self, username):
        return api.user.get(username).getProperty('fullname')

    def display_address(self):
        notarydivision = self.notarydivision
        address = []
        if notarydivision.street_number:
            address.append(notarydivision.street_number)
        if notarydivision.street:
            address.append(notarydivision.street)
        address_display = ', '.join(address)
        return address_display

    def initial_estate_locality(self):
        voc_factory = queryUtility(IVocabularyFactory, "imio.urbdial.notarydivision.Localities")
        voc = voc_factory(self.notarydivision)

        localities = set([voc.getTerm(row['locality']).title for row in self.notarydivision.parcels])

        return ', '.join(list(localities))

    def list_parcels(self):
        parcel_references = []
        for row in self.notarydivision.parcels:
            parcel_references.append(self.get_reference_display(row))
        return parcel_references

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

    def list_ceded_parcellings(self):
        parcellings = self.notarydivision.get_parcellings()
        parcellings = sorted(parcellings, key=lambda parcelling: parcelling.number)
        ceded_parcellings = [p for p in parcellings if p.ceded_parcelling]
        return ceded_parcellings

    def display_deed_type(self, parcelling):
        if parcelling.deed_type == 'autre':
            return parcelling.other_deed_type
        return self.display_value('deed_type', obj=parcelling)

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

    def get_comment_text(self, comment):
        text = comment.text.raw
        text = text.encode('utf-8')
        return text

    def display_deed_types(self):
        parcellings = self.list_ceded_parcellings()
        display_values = [self.display_deed_type(p) for p in parcellings]
        deed_types = ['un acte de {}'.format(deed_type) for deed_type in display_values]

        if len(deed_types) == 1:
            display = deed_types[0]
        elif len(deed_types) == 2:
            display = ' et '.join(deed_types[-2:])
        else:
            display_head = ', '.join(deed_types[0:-2])
            display_tail = ' et '.join(deed_types[-2:])
            display = '{}, {}'.format(display_head, display_tail)

        return display
