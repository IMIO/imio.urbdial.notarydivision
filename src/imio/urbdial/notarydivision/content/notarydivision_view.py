# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.browser.table import CreatedParcelTable
from imio.urbdial.notarydivision.browser.table import EditableCreatedParcelTable
from imio.urbdial.notarydivision.browser.table import EditableInitialParcelTable
from imio.urbdial.notarydivision.browser.table import InitialParcelTable
from imio.urbdial.notarydivision.content.comment_view import CommentContainerView

from plone.dexterity.browser import add
from plone.dexterity.browser import edit
from plone.dexterity.browser import view

from z3c.form import interfaces

from zope.security import checkPermission


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

    def render_InitiaParcel_listing(self):
        if self.context.get_state() == 'In preparation':
            listing = EditableInitialParcelTable(self.context, self.request)
        else:
            listing = InitialParcelTable(self.context, self.request)
        listing.update()
        render = listing.render()
        return render

    def render_CreatedParcel_listing(self):
        if self.context.get_state() == 'In preparation':
            listing = EditableCreatedParcelTable(self.context, self.request)
        else:
            listing = CreatedParcelTable(self.context, self.request)
        listing.update()
        render = listing.render()
        return render

    def can_add_parcel(self, portal_type='InitialParcel'):
        can_add_parcel = checkPermission('imio.urbdial.notarydivision.AddParcel', self.context)
        return can_add_parcel

    def can_add_initial_parcel(self):
        can_add_parcels = self.can_add_parcel()

        notarydivision = self.context
        existing_parcels = notarydivision.get_parcels(portal_type='InitialParcel')
        more_parcels_needed = len(existing_parcels) < notarydivision.initial_parcels

        can_add_initial_parcel = can_add_parcels and more_parcels_needed
        return can_add_initial_parcel

    def can_add_created_parcel(self):
        can_add_parcels = self.can_add_parcel()

        notarydivision = self.context
        existing_parcels = notarydivision.get_parcels(portal_type='CreatedParcel')
        more_parcels_needed = len(existing_parcels) < notarydivision.created_parcels

        can_add_created_parcel = can_add_parcels and more_parcels_needed
        return can_add_created_parcel

    def show_comments_zone(self):
        show_comments_zone = self.context.get_state() != 'In preparation'
        return show_comments_zone
