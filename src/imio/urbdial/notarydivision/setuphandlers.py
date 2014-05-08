# -*- coding: utf-8 -*-

from plone import api

from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager

from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.i18n.interfaces import ITranslationDomain

import logging
logger = logging.getLogger('imio.urbdial.notarydivision: setuphandlers')


def _(msgid, domain, context):
    translation_domain = getUtility(ITranslationDomain, domain)
    return translation_domain.translate(msgid, target_language='fr', default='')


def isNotCurrentProfile(context):
    return context.readDataFile("imiourbdialnotarydivision_marker.txt") is None


def post_install(context):
    """Post install script"""
    if isNotCurrentProfile(context):
        return

    logger.info('delete_plone_root_default_objects : starting...')
    delete_plone_root_default_objects(context)
    logger.info('delete_plone_root_default_objects : Done')
    logger.info('remove_plone_default_portlets : starting...')
    remove_plone_default_portlets(context)
    logger.info('remove_plone_default_portlets : Done')
    logger.info('create_groups : starting...')
    create_groups(context)
    logger.info('create_groups : Done')
    logger.info('create_notarydivisions_folder : starting...')
    create_notarydivisions_folder(context)
    logger.info('create_notarydivisions_folder : Done')
    logger.info('redirect_root_default_view : starting...')
    redirect_root_default_view(context)
    logger.info('redirect_root_default_view : Done')


def delete_plone_root_default_objects(context):
    """
    Delete plone root default objects.
    """
    portal = context.getSite()

    object__ids = ['news', 'events', 'front-page', 'Members']
    for _id in object__ids:
        if _id in portal.objectIds():
            api.content.delete(portal[_id])


def remove_plone_default_portlets(context):
    """
    Remove plone default portlets.
    """
    portal = context.getSite()

    for column in [u'plone.leftcolumn', u'plone.rightcolumn']:
        manager = getUtility(IPortletManager, name=column, context=portal)
        assignments = getMultiAdapter((portal, manager), IPortletAssignmentMapping)
        for portlet in assignments:
            del assignments[portlet]


def create_groups(context):
    """
    Create all customs groups
    """
    create_notaries_group(context)


def create_notaries_group(context):
    """
    """
    portal = context.getSite()

    api.group.create(
        groupname='notaries',
        title=_('Notaries', 'urbdial.divnot', context=portal.REQUEST),
        roles=['Member'],
    )


def create_notarydivisions_folder(context):
    """
     Create a folder which will contain all our NotaryDivision objects.
    """

    portal = context.getSite()

    folder_id = 'notarydivisions'
    if 'notarydivisions' not in portal.objectIds():
        portal.invokeFactory(
            'Folder',
            id=folder_id,
            title=_('notarydivisions_folder_title', 'urbdial.divnot', context=portal.REQUEST),
        )

        folder = getattr(portal, folder_id)

        folder.manage_addLocalRoles('notaries', ['Reader', 'NotaryDivision Creator'])

        _set_AllowedTypes_of_folder(folder, 'NotaryDivision')


def redirect_root_default_view(context):
    """
    Redirect default view of the site on 'notarydivisions' folder
    """

    portal = context.getSite()
    portal.setLayout('redirect_root_view')


def _set_AllowedTypes_of_folder(folder, portal_types):
    """
    Set allowed content types of given folder.
    """

    if type(portal_types) != list:
        portal_types = [portal_types]

    folder.setConstrainTypesMode(1)
    folder.setLocallyAllowedTypes(portal_types)
    folder.setImmediatelyAddableTypes(portal_types)
