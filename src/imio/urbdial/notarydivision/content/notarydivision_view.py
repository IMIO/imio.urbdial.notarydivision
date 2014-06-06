# -*- coding: utf-8 -*-

from plone.dexterity.browser import add
from plone.dexterity.browser import edit
from plone.dexterity.browser import view


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


class NotaryDivisionView(view.DefaultView):
    """
    NotaryDivision custom View.
    """

    def get_comments(self):
        return self.context.objectValues()
