# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.dexterity.browser import add
from plone.dexterity.browser import edit
from plone.dexterity.browser import view


class ParcelView(view.DefaultView):
    """
    Parcel custom View.
    """

    def __call__(self):
        return self.request.response.redirect(
            self.context.get_notarydivision().absolute_url() + '/view#initial_estate'
        )


class ParcelAddForm(add.DefaultAddForm):
    """
    Parcel custom add form.
    """


class ParcelAddView(add.DefaultAddView):
    """
    Parcel custom AddView.
    Required to customize AddForm:
    - first we override the attr 'form' with our custom AddForm.
    - then we register the AddView for our Parcel FTI.
    """
    form = ParcelAddForm

    def render(self):
        return ViewPageTemplateFile("templates/parcel_edit.pt")(self)

    def __getattr__(self, name):
        return getattr(self.form_instance, name)


class ParcelEditForm(edit.DefaultEditForm):
    """
    Parcel custom edit form.
    """

    def render(self):
        return ViewPageTemplateFile("templates/parcel_edit.pt")(self)
