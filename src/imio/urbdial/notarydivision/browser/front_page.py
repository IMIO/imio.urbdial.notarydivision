# -*- coding: utf-8 -*-

from Products.Five import BrowserView

from imio.urbdial.notarydivision.listing.notarydivision import NotaryDivisionTable


class FrontPageView(BrowserView):
    """
    """

    def get_notarydivision_listing(self):
        listing = NotaryDivisionTable(self.context, self.request)
        listing.update()
        render = listing.render()
        return render
