# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from imio.actionspanel.browser.views import ActionsPanelView
from imio.actionspanel.browser.views import DeleteGivenUidView


class UrbdialActionsPanelView(ActionsPanelView):
    """
      This manage the view displaying actions on context.
    """
    def __init__(self, context, request):
        super(UrbdialActionsPanelView, self).__init__(context, request)

        self.SECTIONS_TO_RENDER = (
            'renderEdit',
            'renderOwnDelete',
        )


class UrbdialTransitionsPanelView(ActionsPanelView):
    """
      This manage the view displaying workflow transitions on context.
    """
    def __init__(self, context, request):
        super(UrbdialTransitionsPanelView, self).__init__(context, request)

        self.SECTIONS_TO_RENDER = (
            'renderTransitions',
        )

    def _transitionsToConfirm(self):
        transitions = {
            'NotaryDivision.Notify': 'simpleconfirm_view',
            'NotaryDivision.Pass': 'dateconfirm_view',
            'NotaryDivision.CancelAct': 'simpleconfirm_view',
            'Precision.Publish': 'simpleconfirm_view',
            'FDObservation.Publish': 'simpleconfirm_view',
            'FDPrecisionDemand.Publish': 'simpleconfirm_view',
            'FDInadmissibleFolder.Publish': 'simpleconfirm_view',
            'TownshipObservation.Publish': 'simpleconfirm_view',
            'TownshipPrecisionDemand.Publish': 'simpleconfirm_view',
            'TownshipInadmissibleFolder.Publish': 'simpleconfirm_view',
        }
        return transitions


class UrbdialAddContentPanelView(ActionsPanelView):
    """
    This manage the view displaying actions on context.
    """
    def __init__(self, context, request):
        super(UrbdialAddContentPanelView, self).__init__(context, request)

        self.SECTIONS_TO_RENDER = (
            'renderAddContent',
        )

    def __call__(self):
        return self.renderAddContent()

    def renderAddContent(self):
        """
        Render allowed_content_types coming from portal_type.
        """
        return ViewPageTemplateFile("templates/add_actions.pt")(self)


class DeleteObjectView(DeleteGivenUidView):
    """
    """

    def _computeBackURL(self, obj):
        return obj.aq_parent.absolute_url() + '/#fieldset-estate'
