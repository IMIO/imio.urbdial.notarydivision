# -*- coding: utf-8 -*-

from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes

from imio.urbdial.notarydivision.interfaces import INotaryDivisionFTI
from imio.urbdial.notarydivision.testing_vars import TEST_FD_LOCALGROUP
from imio.urbdial.notarydivision.testing_vars import TEST_FD_NAME
from imio.urbdial.notarydivision.testing_vars import TEST_FD_PASSWORD
from imio.urbdial.notarydivision.testing_vars import TEST_NOTARY_NAME
from imio.urbdial.notarydivision.testing_vars import TEST_NOTARY_PASSWORD
from imio.urbdial.notarydivision.testing_vars import TEST_TOWNSHIP_LOCALGROUP
from imio.urbdial.notarydivision.testing_vars import TEST_TOWNSHIP_NAME
from imio.urbdial.notarydivision.testing_vars import TEST_TOWNSHIP_PASSWORD
from imio.urbdial.notarydivision.utils import translate as _
from imio.urbdial.notarydivision.utils import get_pod_templates_folder
from imio.urbdial.notarydivision.vars import DGO4_LOCAL_GROUPS
from imio.urbdial.notarydivision.vars import TOWNSHIPS_LOCAL_GROUPS

from plone import api

from plone.app.layout.navigation.interfaces import INavigationRoot

from plone.namedfile.file import NamedBlobFile

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
    logger.info('delete_plone_root_default_objects : starting...')
    delete_plone_root_default_objects(context)
    logger.info('delete_plone_root_default_objects : Done')
    logger.info('remove_plone_default_portlets : starting...')
    remove_plone_default_portlets(context)
    logger.info('remove_plone_default_portlets : Done')
    logger.info('create_groups : starting...')
    create_groups(context)
    logger.info('create_groups : Done')
    logger.info('create_local_groups : starting...')
    create_local_groups(context)
    logger.info('create_local_groups : Done')
    logger.info('create_pod_templates_folder : starting...')
    create_pod_templates_folder(context)
    logger.info('create_pod_templates_folder : Done')
    logger.info('create_pod_templates : starting...')
    create_pod_templates(context)
    logger.info('create_pod_templates : Done')
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
    api.group.create(
        groupname='notaries',
        title=_('Notaries'),
        roles=['Member'],
    )

    api.group.create(
        groupname='notaries_admin',
        title=_('Notaries admin'),
        roles=['Member'],
    )

    api.group.create(
        groupname='dgo4',
        title=_('DGO 4'),
        roles=['Member'],
    )

    api.group.create(
        groupname='townships',
        title=_('Townships'),
        roles=['Member'],
    )


def create_local_groups(context):
    """
    Create local sub groups for dgo4, townships and notaries.
    """
    _create_subgroups(container='dgo4', subgroups=DGO4_LOCAL_GROUPS)
    _create_subgroups(container='townships', subgroups=TOWNSHIPS_LOCAL_GROUPS)


def _create_subgroups(container, subgroups):

    for group_infos in subgroups:
        local_group = api.group.create(**group_infos)
        api.group.add_user(user=local_group, groupname=container)


def create_notarydivisions_folder(context):
    """
     Create a folder which will contain all our NotaryDivision objects.
    """

    portal = context.getSite()

    folder_id = 'notarydivisions'
    if folder_id not in portal.objectIds():
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
        folder.manage_addLocalRoles('townships', ['NotaryDivision Reader'])

        set_AllowedTypes_of_folder(folder, 'NotaryDivision')


def create_pod_templates_folder(context):
    """
     Create a folder which will contain all our PODTemplate objects.
    """

    portal = context.getSite()

    folder_id = 'pod_templates'
    if folder_id not in portal.objectIds():
        portal.invokeFactory(
            'ConfigFolder',
            id=folder_id,
            title=_('pod_templates_folder_title'),
        )

        folder = getattr(portal, folder_id)
        folder.manage_addLocalRoles('notaries_admin', ['Config Manager'])
        # need this to be able to call allowedConteTypes methods
        behaviour = ISelectableConstrainTypes(folder)
        set_AllowedTypes_of_folder(behaviour, 'PODTemplate')


def create_pod_templates(context):
    pod_template_folder = get_pod_templates_folder()
    pod_templates = (
        {
            'id': 'precision-fd',
            'title': u'Précision',
            'condition_adapter': 'precision-fd-generation-condition',
        },
        {
            'id': 'precision-ac',
            'title': u'Précision',
            'condition_adapter': 'precision-ac-generation-condition',
        },
        {
            'id': 'notification-fd',
            'title': u'Notification (FD)',
            'condition_adapter': 'notification-generation-condition',
        },
        {
            'id': 'notification-ac',
            'title': u'Notification (AC)',
            'condition_adapter': 'notification-generation-condition',
        },
        {
            'id': 'acte-passe-fd',
            'title': u'Information d\'acte passé (FD)',
            'condition_adapter': 'passed-generation-condition',
        },
        {
            'id': 'acte-passe-ac',
            'title': u'Information d\'acte passé (AC)',
            'condition_adapter': 'passed-generation-condition',
        },
    )

    for template_info in pod_templates:
        templates_path = '%s/pod_templates/%s.odt' % (context._profile_path, template_info['id'])
        odt_file = file(templates_path, 'rb').read()
        blob_file = NamedBlobFile(
            data=odt_file,
            contentType='applications/odt',
            filename=template_info['title'],
        )
        template_info['odt_file'] = blob_file

        template_id = template_info['id']
        if template_id not in pod_template_folder.objectIds():
            api.content.create(
                type='PODTemplate',
                container=pod_template_folder,
                **template_info
            )
            logger.info('create_pod_templates: created template {}'.format(template_id))
        else:
            logger.info('create_pod_templates: template {} already exists'.format(template_id))


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
            'fullname': 'Maitre Nono',
        }
    )
    api.group.add_user(username=TEST_NOTARY_NAME, groupname='notaries')

    api.user.create(
        username=TEST_FD_NAME, password=TEST_FD_PASSWORD, email='fd@dgo4.be',
        properties={
            'fullname': 'Fonctionnaire délégué Dédé',
        }
    )
    api.group.add_user(username=TEST_FD_NAME, groupname=TEST_FD_LOCALGROUP)

    api.user.create(
        username=TEST_TOWNSHIP_NAME, password=TEST_TOWNSHIP_PASSWORD, email='coco@commune.be',
        properties={
            'fullname': 'Agent communal Coco',
        }
    )
    api.group.add_user(username=TEST_TOWNSHIP_NAME, groupname=TEST_TOWNSHIP_LOCALGROUP)
