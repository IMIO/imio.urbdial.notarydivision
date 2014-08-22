# -*- coding: utf-8 -*-

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

    def get_state_date(self):
        state = self.workflow_history.values()[0][-1]
        return state['time']

    def get_state_comment(self):
        state = self.workflow_history.values()[0][-1]
        return state['comments']

    def get_comment_of_state(self, state):
        history = self.workflow_history.values()[0]
        for state_history in reversed(history):
            if state_history.get('review_state') == state:
                return state_history['comments']

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
