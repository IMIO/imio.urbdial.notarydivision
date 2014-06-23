# -*- coding: utf-8 -*-

from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager

from Products.CMFCore.tests.base.security import OmnipotentUser

from plone import api

from zope.component import getUtility
from zope.i18n.interfaces import ITranslationDomain


def translate(msgid, domain='urbdial.divnot'):
    translation_domain = getUtility(ITranslationDomain, domain)
    return translation_domain.translate(msgid, target_language='fr', default=msgid)


def call_with_super_user(callable_obj, *args, **named_args):
    """
    Call a callable object after switching to a security manager with omnipotent user
    then fall back to the original security manager.
    """

    oldsm = getSecurityManager()
    # login as an omnipotent user
    portal = api.portal.getSite()
    newSecurityManager(None, OmnipotentUser().__of__(portal.aq_inner.aq_parent.acl_users))
    try:
        callable_obj(*args, **named_args)
    except Exception, exc:
        # in case something wrong happen, make sure we fall back to original user
        setSecurityManager(oldsm)
        raise exc
    # fall back to original user
    setSecurityManager(oldsm)
