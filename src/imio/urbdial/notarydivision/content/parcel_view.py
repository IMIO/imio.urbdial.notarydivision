# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.statusmessages.interfaces import IStatusMessage

from imio.urbdial.notarydivision import _

from plone.dexterity.browser import add
from plone.dexterity.browser import edit
from plone.dexterity.browser import view

from z3c.form import button


class ParcelView(view.DefaultView):
    """
    Parcel custom View.
    """

    def __call__(self):
        return self.request.response.redirect(
            self.context.get_notarydivision().absolute_url() + '/#fieldset-estate'
        )


class CreatedParcelAddForm(add.DefaultAddForm):
    """
    CreatedParcel custom add form.
    """

    @button.buttonAndHandler(_('Add parcel'), name='add')
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True
            IStatusMessage(self.request).addStatusMessage(_(u"Item created"), "info")


class CreatedParcelAddView(add.DefaultAddView):
    """
    CreatedParcel custom AddView.
    Required to customize AddForm:
    - first we override the attr 'form' with our custom AddForm.
    - then we register the AddView for our CreatedParcel FTI.
    """
    form = CreatedParcelAddForm

    def render(self):
        return ViewPageTemplateFile("templates/parcel_add.pt")(self)

    def __getattr__(self, name):
        return getattr(self.form_instance, name)


class ParcelEditForm(edit.DefaultEditForm):
    """
    Parcel custom edit form.
    """
