# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.testing import TEST_INSTALL_INTEGRATION

import unittest


class TestCommentFields(unittest.TestCase):
    """
    Test schema fields declaration.
    """

    layer = TEST_INSTALL_INTEGRATION

    def test_comment_class(self):
        try:
            from imio.urbdial.notarydivision.content.comment import Comment
        except:
            self.fail("Comment class is not defined.")
