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
from imio.urbdial.notarydivision.workflows.interfaces import INotificationWorkflow
from imio.urbdial.notarydivision.workflows.interfaces import IObservationWorkflow
from imio.urbdial.notarydivision.workflows.interfaces import IPrecisionWorkflow

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


def set_workflows_marker_interfaces(context):
    """
    Provides custom workflows with marker intreface so we can register role/groups
    mapping adapter for these interfaces.
    """

    wf_tool = api.portal.get_tool('portal_workflow')

    observation_wf = wf_tool.getWorkflowById('Observation_workflow')
    alsoProvides(observation_wf, IObservationWorkflow)
    precision_wf = wf_tool.getWorkflowById('Precision_workflow')
    alsoProvides(precision_wf, IPrecisionWorkflow)
    notification_wf = wf_tool.getWorkflowById('Notification_workflow')
    alsoProvides(notification_wf, INotificationWorkflow)


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
            'pod_permission': 'imio.urbdial.notarydivision: Add Precision',
            'pod_expression': 'python: parent.portal_type != "NotaryDivision" and parent.is_dgo4_or_township() == "dgo4"',
        },
        {
            'id': 'precision-ac',
            'title': u'Précision',
            'pod_permission': 'imio.urbdial.notarydivision: Add Precision',
            'pod_expression': 'python: parent.portal_type != "NotaryDivision" and parent.is_dgo4_or_township() == "townships"',
        },
        {
            'id': 'notification',
            'title': u'Notification',
            'pod_permission': 'imio.urbdial.notarydivision: Add Precision',
            'pod_expression': 'python: False',
        },
        {
            'id': 'information-acte-passe-fd',
            'title': u'Information d\'acte passé (FD)',
            'pod_expression': 'python: notarydivision.is_passed()',
        },
        {
            'id': 'information-acte-passe-ac',
            'title': u'Information d\'acte passé (AC)',
            'pod_expression': 'python: notarydivision.is_passed()',
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
    dgo4_localgroup = api.group.create(
        groupname=TEST_FD_LOCALGROUP,
        title=_(TEST_FD_LOCALGROUP),
    )
    api.group.add_user(user=dgo4_localgroup, groupname='dgo4')
    api.group.add_user(username=TEST_FD_NAME, groupname=TEST_FD_LOCALGROUP)

    api.user.create(
        username=TEST_TOWNSHIP_NAME, password=TEST_TOWNSHIP_PASSWORD, email='coco@commune.be',
        properties={
            'fullname': 'Agent communal Coco',
        }
    )
    township_localgroup = api.group.create(
        groupname=TEST_TOWNSHIP_LOCALGROUP,
        title=_(TEST_TOWNSHIP_LOCALGROUP),
    )
    api.group.add_user(user=township_localgroup, groupname='townships')
    api.group.add_user(username=TEST_TOWNSHIP_NAME, groupname=TEST_TOWNSHIP_LOCALGROUP)
