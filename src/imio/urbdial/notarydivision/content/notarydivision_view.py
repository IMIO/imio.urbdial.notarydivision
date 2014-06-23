# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision import _
from imio.urbdial.notarydivision.content.comment_view import CommentContainerView
from imio.urbdial.notarydivision.utils import translate

from plone import api

from plone.dexterity.browser import add
from plone.dexterity.browser import edit

from zope.security import checkPermission


class NotaryDivisionAddForm(add.DefaultAddForm):
    """
    NotaryDivision custom Add form.
    """


class NotaryDivisionAddView(add.DefaultAddView):
    """
    NotaryDivision custom AddView.
    Required to customize AddForm:
    - first we override the attr 'form' with our custom AddForm.
    - then we register the AddView for our NotaryDivision FTI.
    """
    form = NotaryDivisionAddForm


class NotaryDivisionEditForm(edit.DefaultEditForm):
    """
    NotaryDivision custom Edit form.
    """


class NotaryDivisionView(CommentContainerView):
    """
    NotaryDivision custom View.
    """

    def display_add_types(self):
        """Return actions"""

        actions = []
        add = translate(u'Add')

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
                action = '<a name={}_{} href={} class={} >\
                    {} {}\
                    </a>'.format(
                        add,
                        content_type,
                        url,
                        "apButton apButtonAction",
                        add,
                        translate(content_type).encode('utf-8')
                    )
                actions.append(action)
        actions = ''.join(actions)
        actions = '<span>{}</span>'.format(actions)
        return actions
