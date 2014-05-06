# -*- coding: utf-8 -*-

from plone import api

from zope.component import queryUtility
from zope.i18n.interfaces import ITranslationDomain

import logging
logger = logging.getLogger('imio.urbdial.notarydivision: setuphandlers')


def _(msgid, domain, context):
    translation_domain = queryUtility(ITranslationDomain, domain)
    return translation_domain.translate(msgid, target_language='fr', default='')


def isNotCurrentProfile(context):
    return context.readDataFile("imiourbdialnotarydivision_marker.txt") is None


def post_install(context):
    """Post install script"""
    if isNotCurrentProfile(context):
        return

    logger.info('deletePloneRootDefaultObjects : starting...')
    deletePloneRootDefaultObjects(context)
    logger.info('deletePloneRootDefaultObjects : Done')
    logger.info('createNotarydivisionsFolder : starting...')
    createNotarydivisionsFolder(context)
    logger.info('createNotarydivisionsFolder : Done')


def deletePloneRootDefaultObjects(context):
    """
    Get rid of plone root default objects.
    """

    portal = context.getSite()

    object__ids = ['news', 'events', 'front-page', 'Members']
    for _id in object__ids:
        if _id in portal.objectIds():
            api.content.delete(portal[_id])


def createNotarydivisionsFolder(context):
    """
     Create a folder which will contain all our NotaryDivision objects.
    """

    portal = context.getSite()

    folder_id = 'notarydivisions'
    if 'notarydivisions' not in portal.objectIds():
        portal.invokeFactory(
            'Folder',
            id=folder_id,
            title=_('notarydivisions_folder_title', 'urbdial.divnot', context=portal.REQUEST)
        )
        folder = getattr(portal, folder_id)
        _setFolderAllowedTypes(folder, 'NotaryDivision')


def _setFolderAllowedTypes(folder, portal_types):
    """
    Set allowed content types of given folder.
    """

    if type(portal_types) != list:
        portal_types = [portal_types]

    folder.setConstrainTypesMode(1)
    folder.setLocallyAllowedTypes(portal_types)
    folder.setImmediatelyAddableTypes(portal_types)
