# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from imio.urbdial.notarydivision import _
from imio.urbdial.notarydivision.content.comment import IComment
from imio.urbdial.notarydivision.utils import translate

from plone import api
from plone.dexterity.browser import add
from plone.dexterity.browser import edit
from plone.dexterity.browser import view

from zope.security import checkPermission


class CommentContainerView(object):
    """
    Base helper class for the view of any comment container.
    """

    def get_view_of(self, comment):
        """
        Return BrowserView of a subcomment.
        """
        comment_view = comment.restrictedTraverse('view')
        comment_view.update()
        return comment_view


class CommentContainerView(CommentContainerView):
    """
    Base helper class for the display view of any comment container.
    """

    def get_comments(self):
        all_comments = self.context.objectValues()
        visible_comments = [c for c in all_comments if checkPermission('zope2.View', c)]
        return visible_comments


class CommentView(view.DefaultView, CommentContainerView):
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
        action, author, warning, date = self.get_last_action_infos(comment)

        title = '{type_} par {author}, {action} le {date} {warning}:'.format(
            type_=type_.encode('utf-8'),
            author=author,
            action=action,
            date=date,
            warning=warning,
        )
        return title

    def get_last_action_infos(self, comment):
        if comment.is_in_draft():
            action = 'créé'
            author = comment.creators[0]
            warning = '(BROUILLON NON PUBLIÉ)'
            date = comment.get_creation_date()
        else:
            action = 'publié'
            author = comment.get_publicator()
            warning = ''
            date = comment.get_publication_date()
        date = date.strftime('%d/%m/%Y à %H:%M')
        author = api.user.get(author).getProperty('fullname')

        return action, author, warning, date

    def display_field(self, field_id):
        val = getattr(self.context, field_id)
        if val is None or val == '' or val == u'':
            display_value = '<p><span class="discreet">N.C</span></p>'
        else:
            widget = self.widgets[field_id]
            display_value = widget.render()
        return display_value


class CommentAddForm(add.DefaultAddForm):
    """
    Comment custom add form.
    """


class CommentAddView(add.DefaultAddView, CommentContainerView):
    """
    Comment custom AddView.
    Required to customize AddForm:
    - first we override the attr 'form' with our custom AddForm.
    - then we register the AddView for our Comment FTI.
    """
    form = CommentAddForm

    def render(self):
        return ViewPageTemplateFile("templates/comment_edit.pt")(self)

    def __getattr__(self, name):
        return getattr(self.form_instance, name)

    def get_previous_comments(self):
        previous_comments = []
        container = self.context

        while IComment.providedBy(container):
            previous_comments.append(container)
            container = container.aq_parent

        return previous_comments


class CommentEditForm(edit.DefaultEditForm, CommentContainerView):
    """
    Comment custom edit form.
    """

    def render(self):
        return ViewPageTemplateFile("templates/comment_edit.pt")(self)

    def get_previous_comments(self):
        previous_comments = []
        container = self.context.aq_parent

        while IComment.providedBy(container):
            previous_comments.append(container)
            container = container.aq_parent

        return previous_comments
