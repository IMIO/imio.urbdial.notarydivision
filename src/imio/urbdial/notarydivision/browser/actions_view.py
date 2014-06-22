# -*- coding: utf-8 -*-

from imio.actionspanel.browser.views import ActionsPanelView


class UrbdialActionsPanelView(ActionsPanelView):
    """
      This manage the view displaying actions on context.
    """
    def __init__(self, context, request):
        super(UrbdialActionsPanelView, self).__init__(context, request)

        # Only keep 'delete' action.
        self.ACCEPTABLE_ACTIONS = ('delete',)
