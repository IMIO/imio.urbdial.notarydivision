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

    def test_date(self):
        view = self.get_helper_view(self.test_divnot)
        date = DateTime('18/09/1986')
        self.assertTrue(view.date(date) == '18/09/1986')

    def test_fullname(self):
        view = self.get_helper_view(self.test_divnot)
        self.assertTrue(view.fullname('fd_dede') == 'Fonctionnaire délégué Dédé')

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
        msg = "Localities display should have be '{}' but is '{}'.".format(
            expected_display,
            localities_display,
        )
        self.assertTrue(localities_display == expected_display, msg)

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
                'bis': None,
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
        expected_display = ' Beez A 42 G 66,  Yolo B 999 H 42'
        msg = "Refrences display should have be '{}' but is '{}'.".format(
            expected_display,
            cadastral_refs,
        )
        self.assertTrue(cadastral_refs == expected_display, msg)

    def test_list_attachments(self):
        observation = self.test_observation
        view = self.get_helper_view(observation)

        class FakeFile(object):
            def __init__(self, filename):
                self.filename = filename

        observation.files = [FakeFile('yolo'), FakeFile('ncha')]
        attachments_display = view.list_attachments()
        expected_display = 'yolo, ncha'
        msg = "Attachments display should have be '{}' but is '{}'.".format(
            expected_display,
            attachments_display,
        )
        self.assertTrue(attachments_display == expected_display, msg)
