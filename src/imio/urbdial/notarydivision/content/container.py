# -*- coding: utf-8 -*-

from plone.dexterity.content import Container

from plone import api


class BaseContainer(Container):
    """
    Base class for urbdial content types
    """

    def get_state(self):
        state = api.content.get_state(self)
        return state

    def transition(self, transition):
        api.content.transition(self, transition)
