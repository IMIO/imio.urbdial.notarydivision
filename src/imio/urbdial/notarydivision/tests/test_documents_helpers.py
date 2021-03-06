# -*- coding: utf-8 -*-

from DateTime import DateTime

from imio.urbdial.notarydivision.testing import CommentBrowserTest

from zope.component import queryMultiAdapter
from zope.interface import Interface


class GenerationHelperMethods(CommentBrowserTest):
    """
    Test methods of generation helper view.
    """

    def get_helper_view(self, context):
        helper_view = queryMultiAdapter(
            (context, context.REQUEST),
            Interface,
            'document-generation-methods',
        )
        return helper_view

    def test_init_on_notary_division(self):
        """
        view.notarydivision should be the notarydivision on which the helper view
        was called.
        """
        notarydivision = self.test_divnot
        view = self.get_helper_view(notarydivision)
        self.assertTrue(view.notarydivision is notarydivision)

    def test_init_on_comment(self):
        """
        view.notarydivision should be the notarydivision of the comment on which
        the helper view was called.
        """
        notarydivision = self.test_divnot
        observation = self.test_observation
        view = self.get_helper_view(observation)
        self.assertTrue(view.notarydivision is notarydivision)

    def _test_display(self, result, expected):
        msg = "Expected display '{}' but got '{}'".format(expected, result)
        self.assertTrue(result == expected, msg)

    def test_display_voc_value(self):
        notarydivision = self.test_divnot
        view = self.get_helper_view(notarydivision)

        notarydivision.article_90 = set(['3deg'])
        expected_display = u"3° : la division s'inscrit dans le cadre d'un partage pour sortir d'une indivision d'origine successorale ne créant pas plus de lots que de copartageants"
        result = view.display_voc_value_of_field(value='3deg', field_name='article_90')
        self.assertTrue(result == expected_display)

    def test_display_voc_values(self):
        notarydivision = self.test_divnot
        view = self.get_helper_view(notarydivision)

        notarydivision.local_township = set(['ac_namur', 'ac_sambreville'])
        expected_display = u"Namur, Sambreville"
        result = view.display_values(field_name='local_township')
        self.assertTrue(result == expected_display)

    def test_date(self):
        view = self.get_helper_view(self.test_divnot)
        date = DateTime('18/09/1986')
        self._test_display(view.date(date), expected='18/09/1986')

    def test_fullname(self):
        view = self.get_helper_view(self.test_divnot)
        self._test_display(view.fullname('fd_dede'), expected='Fonctionnaire délégué Dédé')

    def test_initial_estate_locality(self):
        notarydivision = self.test_divnot
        view = self.get_helper_view(notarydivision)
        notarydivision.parcels = [
            {
                'division': None,
                'power': None,
                'locality': '5000',
                'radical': None,
                'section': None,
                'bis': None,
                'exposant': None
            },
            {
                'division': None,
                'power': None,
                'locality': '4970',
                'radical': None,
                'section': None,
                'bis': None,
                'exposant': None
            }
        ]
        localities_display = view.initial_estate_locality()
        expected_display = 'Stavelot, Namur'
        self._test_display(localities_display, expected_display)

    def test_list_parcels(self):
        notarydivision = self.test_divnot
        view = self.get_helper_view(notarydivision)
        notarydivision.parcels = [
            {
                'division': 'Beez',
                'power': '66',
                'locality': None,
                'radical': '42',
                'section': 'A',
                'bis': '2',
                'exposant': 'G'
            },
            {
                'division': 'Yolo',
                'power': '42',
                'locality': None,
                'radical': '999',
                'section': 'B',
                'bis': None,
                'exposant': 'H'
            }
        ]
        parcels = view.list_parcels()
        expected_display = ' Beez A 42/2 G 66,  Yolo B 999 H 42'
        self._test_display(', '.join(parcels), expected_display)

    def test_list_attachments(self):
        observation = self.test_observation
        view = self.get_helper_view(observation)

        class FakeFile(object):
            def __init__(self, filename):
                self.filename = filename

        observation.files = [FakeFile('yolo'), FakeFile('ncha')]
        attachments_display = view.list_attachments()
        expected_display = 'yolo, ncha'
        self._test_display(attachments_display, expected_display)

    def test_list_applicants(self):
        notarydivision = self.test_divnot
        view = self.get_helper_view(notarydivision)
        applicants = []

        # no applicants
        notarydivision.applicants = applicants
        self._test_display(view.list_applicants(), expected='')

        # 1 applicant
        applicants.append({'name': 'Cenfrapé', 'firstname': 'André'})
        notarydivision.applicants = applicants
        self._test_display(view.list_applicants(), expected='André Cenfrapé')

        # 2 applicants
        applicants.append({'name': 'Terrieur', 'firstname': 'Alain'})
        notarydivision.applicants = applicants
        expected = 'André Cenfrapé et Alain Terrieur'
        self._test_display(view.list_applicants(), expected)

        # 3 or more applicants
        applicants.append({'name': 'Porte', 'firstname': 'Sarah'})
        notarydivision.applicants = applicants
        expected = 'André Cenfrapé, Alain Terrieur et Sarah Porte'
        self._test_display(view.list_applicants(), expected)
