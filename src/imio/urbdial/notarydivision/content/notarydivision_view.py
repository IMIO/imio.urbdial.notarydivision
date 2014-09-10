# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision import _
from imio.urbdial.notarydivision.browser.table import CreatedParcelTable
from imio.urbdial.notarydivision.browser.table import EditableCreatedParcelTable
from imio.urbdial.notarydivision.content.comment_view import CommentContainerView
from imio.urbdial.notarydivision.utils import translate

from plone import api
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

    def __init__(self, context, request):
        super(NotaryDivisionView, self).__init__(context, request)
        self.context = context
        self.request = request
        plone_utils = api.portal.get_tool('plone_utils')
        if self.can_add_created_parcel():
            plone_utils.addPortalMessage(_('warning_not_enough_created_parcels'), type="warning")

    def render_CreatedParcel_listing(self):
        if self.context.get_state() == 'In preparation':
            listing = EditableCreatedParcelTable(self.context, self.request)
        else:
            listing = CreatedParcelTable(self.context, self.request)
        listing.update()
        render = listing.render()
        return render

    def can_add_parcel(self):
        try:
            can_add_parcel = checkPermission('imio.urbdial.notarydivision.AddParcel', self.context)
        except:
            return False
        return can_add_parcel

    def can_add_created_parcel(self):
        can_add_parcels = self.can_add_parcel()

        notarydivision = self.context
        existing_parcels = notarydivision.get_parcels(portal_type='CreatedParcel')
        more_parcels_needed = len(existing_parcels) < notarydivision.created_parcellings

        can_add_created_parcel = can_add_parcels and more_parcels_needed
        return can_add_created_parcel

    def show_comments_zone(self):
        show_comments_zone = self.context.get_state() != 'In preparation'
        return show_comments_zone

    def get_last_state_date(self):
        raw_date = self.context.get_state_date()
        date = ''
        if raw_date:
            date = raw_date.strftime('%d/%m/%Y')
        return date

    def get_address_display(self):
        number = self.context.street_number
        number = number and u'{}'.format(number) or u''
        street = self.context.street
        street = street and street or u''
        if street and number:
            address = u'{}, {}'.format(number, street)
        else:
            address = u'{}{}'.format(number, street)
        return address

    def get_undivided_display(self):
        undivided = self.context.undivided
        undivided_display = undivided and 'Yes' or 'No'
        undivided_display = translate(undivided_display, domain='plone')
        if undivided:
            base_url = self.context.absolute_url()
            link = '<a class="link-overlay" href="{ref}/@@specificrights">{rights}</a>'.format(
                ref=base_url,
                rights=translate('Specific rights')
            )
            undivided_display = '<span id="urbdial-undivided">{undivided}.&nbsp&nbsp&nbsp{link}</span>'.format(
                undivided=undivided_display,
                link=link
            )
        return undivided_display

    def get_initial_estate_widgets(self):
        """
        Return initial estate fields of tab 'estate'.
        """

        estate_tab = [tab for tab in self.groups if tab.__name__ == 'estate'][0]
        initial_estate_fields = ['actual_use', 'surface', 'parcels']
        widgets = [w for w in estate_tab.widgets.values() if w.__name__ in initial_estate_fields]
        return widgets
