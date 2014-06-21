# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision import _
from imio.urbdial.notarydivision.utils import translate

from plone import api
from plone.dexterity.browser import view

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

    def display_title(self):
        comment = self.context
        type_ = translate(_(comment.portal_type))

        author = api.user.get(comment.creators[0])
        author = author.getUserName()
        history = comment.workflow_history.values()[0][-1]
        action = history.get('action') == 'Publish' and 'publié' or 'créé'
        date = history.get('time').strftime('%d/%m/%Y à %H:%M')
        warning = history.get('action') == 'Publish' and ' ' or ' (BROUILLON NON PUBLIÉ)'

        publication = '{action} le {date}{warning}'.format(
            action=action,
            date=date,
            warning=warning,
        )

        title = '{type_} par {author}, {publication}:'.format(
            type_=type_.encode('utf-8'),
            author=author,
            publication=publication,
        )
        return title

    def display_field(self, field_id):
        val = getattr(self.context, field_id)
        if val is None or val == '' or val == u'':
            display_value = '<p><span class="discreet">N.C</span></p>'
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
                action = '<a name=add_{} href={} class={} >Add {}</a>'.format(
                    content_type,
                    url,
                    "apButton apButtonAction",
                    content_type
                )
                actions.append(action)
        actions = ''.join(actions)
        actions = '<span>{}</span>'.format(actions)
        return actions
