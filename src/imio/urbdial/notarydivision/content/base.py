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
