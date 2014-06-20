# -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.interfaces import INotaryDivisionFTI
from imio.urbdial.notarydivision.testing_vars import TEST_FD_NAME
from imio.urbdial.notarydivision.testing_vars import TEST_FD_PASSWORD
from imio.urbdial.notarydivision.testing_vars import TEST_NOTARY_NAME
from imio.urbdial.notarydivision.testing_vars import TEST_NOTARY_PASSWORD
from imio.urbdial.notarydivision.utils import translate as _
from imio.urbdial.notarydivision.workflows.interfaces import IObservationWorkflow

from plone import api

from plone.app.layout.navigation.interfaces import INavigationRoot

from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager

from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import alsoProvides

import logging
logger = logging.getLogger('imio.urbdial.notarydivision: setuphandlers')


def isNotCurrentProfile(context):
    return context.readDataFile("imiourbdialnotarydivision_marker.txt") is None


def post_install(context):
    """Post install script"""
    if isNotCurrentProfile(context):
        return

    logger.info('set_NotaryDivision_FTI_marker_interface : starting...')
    set_NotaryDivision_FTI_marker_interface(context)
    logger.info('set_NotaryDivision_FTI_marker_interface : Done')
    logger.info('set_workflows_marker_interfaces : starting...')
    set_workflows_marker_interfaces(context)
    logger.info('set_workflows_marker_interfaces : Done')
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


def set_NotaryDivision_FTI_marker_interface(context):
    """
    Set INotaryDivisionFTI interface on NotaryDivision FTI, so we can register
    custom AddView for this specific interface.
    """
    site = context.getSite()
    divnot_type = site.portal_types.NotaryDivision
    alsoProvides(divnot_type, INotaryDivisionFTI)


def set_workflows_marker_interfaces(context):
    """
    Provides custom workflows with marker intreface so we can register role/groups
    mapping adapter for these interfaces.
    """

    wf_tool = api.portal.get_tool('portal_workflow')

    observation_wf = wf_tool.getWorkflowById('Observation_workflow')
    alsoProvides(observation_wf, IObservationWorkflow)


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
    create_dgo4_group(context)


def create_notaries_group(context):
    api.group.create(
        groupname='notaries',
        title=_('Notaries'),
        roles=['Member'],
    )


def create_dgo4_group(context):
    api.group.create(
        groupname='dgo4',
        title=_('DGO 4'),
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
            title=_('notarydivisions_folder_title'),
        )

        folder = getattr(portal, folder_id)

        # this folder will behave as the site root
        alsoProvides(folder, INavigationRoot)

        folder.manage_addLocalRoles('notaries', ['NotaryDivision Reader', 'NotaryDivision Creator'])
        folder.manage_addLocalRoles('dgo4', ['NotaryDivision Reader'])

        set_AllowedTypes_of_folder(folder, 'NotaryDivision')


def redirect_root_default_view(context):
    """
    Redirect default view of the site on 'notarydivisions' folder
    """

    portal = context.getSite()
    portal.setLayout('redirect_root_view')


def set_AllowedTypes_of_folder(folder, portal_types):
    """
    Set allowed content types of given folder.
    """

    if type(portal_types) != list:
        portal_types = [portal_types]

    folder.setConstrainTypesMode(1)
    folder.setLocallyAllowedTypes(portal_types)
    folder.setImmediatelyAddableTypes(portal_types)


def testing_post_install(context):
    """Post install script"""
    if context.readDataFile("urbdialnotarydivision_testing_marker.txt") is None:
        return

    logger.info('create_test_users : starting...')
    create_test_users(context)
    logger.info('create_test_users : Done')


def create_test_users(context):
    """
    Create tests user for the different groups.
    """
    api.user.create(
        username=TEST_NOTARY_NAME, password=TEST_NOTARY_PASSWORD, email='notary@frnb.be',
        properties={
            'fullname': 'Maitre Notaire',
        }
    )
    api.group.add_user(username=TEST_NOTARY_NAME, groupname='notaries')

    api.user.create(
        username=TEST_FD_NAME, password=TEST_FD_PASSWORD, email='fd@dgo4.be',
        properties={
            'fullname': 'Fonctionnaire délégué Dédé',
        }
    )
    api.group.add_user(username=TEST_FD_NAME, groupname='dgo4')
