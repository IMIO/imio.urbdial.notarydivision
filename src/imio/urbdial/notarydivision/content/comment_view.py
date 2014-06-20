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
            self.context.get_notarydivision().absolute_url() + '/view#comments'
        )

    def display_field(self, field_id):
        val = getattr(self.context, field_id)
        if val is None or val == '' or val == u'':
            display_value = '<span class="discreet">N.C</span>'
        else:
            widget = self.widgets[field_id]
            display_value = widget.render()
        return display_value

    def display_add_types(self):
        """Return actions add types"""

        actions = []

        types_tool = api.portal.get_tool('portal_types')
        portal_type = types_tool.get(self.context.portal_type)
        allowed_content_types = portal_type.allowed_content_types
        for content_type in allowed_content_types:
            portal_type = types_tool.get(content_type)
            add_permission = portal_type.add_permission
            if checkPermission(add_permission, self.context):
                url = '{}/++add++{}'.format(
                    self.context.absolute_url(),
                    content_type
                )
                action = '<a name=add_{} href={} class={} >\
                    Add {}\
                    </a>'.format(
                        content_type,
                        url,
                        "apButton apButtonAction",
                        content_type
                    )
                actions.append(action)
        actions = ''.join(actions)
        actions = '<span>{}</span>'.format(actions)
        return actions

    def display_actions(self):
        """Return iconified actions."""

        actions = []

        if checkPermission('cmf.ModifyPortalContent', self.context):
            edit_action = self.get_edit_action()
            actions.append(edit_action)

        if checkPermission('zope2.DeleteObjects', self.context):
            delete_action = self.get_delete_action()
            actions.append(delete_action)

        actions = ''.join(actions)
        actions = '<span>{}</span>'.format(actions)

        return actions

    def get_edit_action(self):
        portal = api.portal.getSite()
        site_url = portal.absolute_url()
        comment_url = self.context.absolute_url()

        edit_icon_url = '{site_url}/edit.png'.format(site_url=site_url)
        edit_url = '{comment_url}/edit'.format(comment_url=comment_url)

        edit_action = '<a name="edit_comment" href={} class="apButton apButtonAction action_edit"><img src="{}"></a>'.format(
            edit_url,
            edit_icon_url,
        )
        return edit_action

    def get_delete_action(self):
        portal = api.portal.getSite()
        site_url = portal.absolute_url()
        comment_url = self.context.absolute_url()

        delete_icon_url = '{site_url}/++resource++imio.urbdial.notarydivision/delete_icon.gif'.format(site_url=site_url)
        delete_url = '{comment_url}/delete_confirmation'.format(comment_url=comment_url)

        delete_action = '<a name="delete_comment" href={} class="apButton apButtonAction action_delete"><img src="{}"></a>'.format(
            delete_url,
            delete_icon_url,
        )
        return delete_action
