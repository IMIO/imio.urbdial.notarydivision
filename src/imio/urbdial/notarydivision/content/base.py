# -*- coding: utf-8 -*-

from DateTime import DateTime

from plone.dexterity.content import Container
from plone.dexterity.content import Item

from plone import api


class UrbdialObject(object):
    """
    Base class for urbdial content types.
    """

    def get_state(self):
        state = api.content.get_state(self)
        return state

    def get_date_of_last_transition(self, transition):
        history = self.workflow_history.values()[0]
        for state_history in reversed(history):
            if state_history.get('action') == transition:
                date = self._get_transition_date(state_history)
                return date

    def get_last_transition_date(self):
        last_state = self.workflow_history.values()[0][-1]
        transition = last_state['action']
        if transition:
            date = self._get_transition_date(last_state)
            return date

    def _get_transition_date(self, state_history):
        comment = state_history.get('comments', None)
        if comment:
            return DateTime(comment)
        return state_history['time']

    def transition(self, transition):
        api.content.transition(self, transition)


class UrbdialContainer(Container, UrbdialObject):
    """
    Base class for urbdial folderish content types
    """


class UrbdialItem(Item, UrbdialObject):
    """
    Base class for urbdial non folderish content types
    """
