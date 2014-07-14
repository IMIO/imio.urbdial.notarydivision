# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.content.comment_view import CommentContainerView

from plone.dexterity.browser import add
from plone.dexterity.browser import edit
from plone.dexterity.browser import view

from z3c.form import interfaces


class NotaryDivisionAddForm(add.DefaultAddForm):
    """
    NotaryDivision custom Add form.
    """
    def update(self):
        super(NotaryDivisionAddForm, self).update()
        for group in self.groups:
            if 'local_dgo4' in group.widgets:
                group.widgets['local_dgo4'].mode = interfaces.HIDDEN_MODE
                group.widgets['local_township'].mode = interfaces.HIDDEN_MODE


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
    def update(self):
        super(NotaryDivisionEditForm, self).update()
        for group in self.groups:
            if 'local_dgo4' in group.widgets:
                group.widgets['local_dgo4'].mode = interfaces.HIDDEN_MODE
                group.widgets['local_township'].mode = interfaces.HIDDEN_MODE


class NotaryDivisionView(view.DefaultView, CommentContainerView):
    """
    NotaryDivision custom View.
    """
