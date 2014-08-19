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
            self.context.get_notarydivision().absolute_url() + '/view'
        )


class InitialParcelAddForm(add.DefaultAddForm):
    """
    InitialParcel custom add form.
    """


class InitialParcelAddView(add.DefaultAddView):
    """
    InitialParcel custom AddView.
    Required to customize AddForm:
    - first we override the attr 'form' with our custom AddForm.
    - then we register the AddView for our InitialParcel FTI.
    """
    form = InitialParcelAddForm

    def render(self):
        return ViewPageTemplateFile("templates/parcel_edit.pt")(self)

    def __getattr__(self, name):
        return getattr(self.form_instance, name)


class CreatedParcelAddForm(add.DefaultAddForm):
    """
    CreatedParcel custom add form.
    """


class CreatedParcelAddView(add.DefaultAddView):
    """
    CreatedParcel custom AddView.
    Required to customize AddForm:
    - first we override the attr 'form' with our custom AddForm.
    - then we register the AddView for our CreatedParcel FTI.
    """
    form = CreatedParcelAddForm

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
