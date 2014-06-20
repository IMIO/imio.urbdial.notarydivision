# -*- coding: utf-8 -*-

from plone.dexterity.browser import view
from plone import api

from zope.security import checkPermission


class CommentContainerView(view.DefaultView):
    """
    Base class for content type view which can contain comment.
    """

    def get_comments(self):
        all_comments = self.context.objectValues()
        visible_comments = [c for c in all_comments if checkPermission('zope2.View', c)]
        return visible_comments

    def get_view_of(self, comment):
        """Return BrowserView of a subcomment."""

        comment_view = comment.restrictedTraverse('view')
        comment_view.update()
        return comment_view


class CommentView(CommentContainerView):
    """
    Comment custom View.
    """

    def __call__(self):
        return self.request.response.redirect(
            self.context.get_notarydivision().absolute_url() + '/view#observations'
        )

    def display_field(self, field_id):
        val = getattr(self.context, field_id)
        if val is None or val == '' or val == u'':
            display_value = '<span class="discreet">N.C</span>'
        else:
            widget = self.widgets[field_id]
            display_value = widget.render()
        return display_value
