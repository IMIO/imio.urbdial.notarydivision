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
        notarydivision.initial_estate = [
            {
                'division': None,
                'power': None,
                'locality': '5000',
                'radical': None,
                'section': None,
                'surface': None,
                'specific_rights': None,
                'bis': None,
                'exposant': None
            },
            {
                'division': None,
                'power': None,
                'locality': '4970',
                'radical': None,
                'section': None,
                'surface': None,
                'specific_rights': None,
                'bis': None,
                'exposant': None
            }
        ]
        localities_display = view.initial_estate_locality()
        expected_display = 'Namur, Stavelot'
        self._test_display(localities_display, expected_display)

    def test_initial_estate_cadastral_ref(self):
        notarydivision = self.test_divnot
        view = self.get_helper_view(notarydivision)
        notarydivision.initial_estate = [
            {
                'division': 'Beez',
                'power': '66',
                'locality': None,
                'radical': '42',
                'section': 'A',
                'surface': None,
                'specific_rights': None,
                'bis': '2',
                'exposant': 'G'
            },
            {
                'division': 'Yolo',
                'power': '42',
                'locality': None,
                'radical': '999',
                'section': 'B',
                'surface': None,
                'specific_rights': None,
                'bis': None,
                'exposant': 'H'
            }
        ]
        cadastral_refs = view.initial_estate_cadastral_ref()
        expected_display = ' Beez A 42/2 G 66,  Yolo B 999 H 42'
        self._test_display(cadastral_refs, expected_display)

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
