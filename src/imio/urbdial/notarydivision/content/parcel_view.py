# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.statusmessages.interfaces import IStatusMessage

from imio.urbdial.notarydivision import _
from imio.urbdial.notarydivision.browser.table import NextCreatedParcelsTable
from imio.urbdial.notarydivision.browser.table import NextInitialParcelsTable
from imio.urbdial.notarydivision.browser.table import PreviousCreatedParcelsTable
from imio.urbdial.notarydivision.browser.table import PreviousInitialParcelsTable

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


class InitialParcelAddForm(add.DefaultAddForm):
    """
    InitialParcel custom add form.
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


class InitialParcelAddView(add.DefaultAddView):
    """
    InitialParcel custom AddView.
    Required to customize AddForm:
    - first we override the attr 'form' with our custom AddForm.
    - then we register the AddView for our InitialParcel FTI.
    """
    form = InitialParcelAddForm

    def render(self):
        return ViewPageTemplateFile("templates/parcel_add.pt")(self)

    def __getattr__(self, name):
        return getattr(self.form_instance, name)


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

    def render(self):
        return ViewPageTemplateFile("templates/parcel_edit.pt")(self)

    def render_previous_parcels_listing(self):
        portal_type = self.context.portal_type
        if portal_type == 'InitialParcel':
            listing = PreviousInitialParcelsTable()
        elif portal_type == 'CreatedParcel':
            listing = PreviousCreatedParcelsTable()
        listing.update()
        return listing

    def render_next_parcels_listing(self):
        portal_type = self.context.portal_type
        if portal_type == 'InitialParcel':
            listing = NextInitialParcelsTable()
        elif portal_type == 'CreatedParcel':
            listing = NextCreatedParcelsTable()
        listing.update()
        return listing
