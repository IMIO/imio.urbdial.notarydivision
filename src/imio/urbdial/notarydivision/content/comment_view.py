# -*- coding: utf-8 -*-

from plone.dexterity.browser import view


class CommentContainerView(view.DefaultView):
    """
    Base class for content type view which can contain comment.
    """

    def get_comments(self):
        all_comments = self.context.objectValues()
        visible_comments = [c for c in all_comments if c.check_View_permission()]
        return visible_comments


class CommentView(CommentContainerView):
    """
    Comment custom View.
    """

    def __call__(self):
        return self.request.response.redirect(
            self.context.getNotaryDivision().absolute_url() + '/view#observations'
        )
