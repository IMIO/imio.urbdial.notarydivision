# -*- coding: utf-8 -*-

from plone.dexterity.browser import view


class CommentView(view.DefaultView):
    """
    Comment custom View.
    """

    def __call__(self):
        return self.request.response.redirect(
            self.context.getNotaryDivision().absolute_url() + '/view#observations'
        )

    def render(self):
        pass
