# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from imio.actionspanel.browser.views import ActionsPanelView


class UrbdialActionsPanelView(ActionsPanelView):
    """
      This manage the view displaying actions on context.
    """
    def __init__(self, context, request):
        super(UrbdialActionsPanelView, self).__init__(context, request)

        self.SECTIONS_TO_RENDER = (
            'renderTransitions',
            'renderEdit',
            'renderOwnDelete',
        )


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
