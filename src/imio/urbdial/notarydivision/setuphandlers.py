# -*- coding: utf-8 -*-

from plone import api

import logging
logger = logging.getLogger('imio.urbdial.notarydivision: setuphandlers')


def isNotCurrentProfile(context):
    return context.readDataFile("imiourbdialnotarydivision_marker.txt") is None


def post_install(context):
    """Post install script"""
    if isNotCurrentProfile(context):
        return

    logger.info("deletePloneRootDefaultObjects : starting...")
    deletePloneRootDefaultObjects(context)
    logger.info("deletePloneRootDefaultObjects : Done")


def deletePloneRootDefaultObjects(context):

    portal = context.getSite()

    object__ids = ['news', 'events', 'front-page', 'Members']
    for _id in object__ids:
        if _id in portal.objectIds():
            api.content.delete(portal[_id])
