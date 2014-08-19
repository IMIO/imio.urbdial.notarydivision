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

    def _transitionsToConfirm(self):
        """
          Return the list of transitions the user will have to confirm, aka
          the user will be able to enter a comment for.
          This is a per meta_type or portal_type list of transitions to confirm.
          So for example, this could be :
          ('ATDocument.reject', 'Document.publish', 'Collection.publish', )
          --> ATDocument is a meta_type and Document is a portal_type for example
        """
        return ('NotaryDivision.Notify', 'NotaryDivision.Pass', 'Precision.Publish')


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
