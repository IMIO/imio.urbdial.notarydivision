# -*- coding: utf-8 -*-

NOTARY_DIVISION_TYPES = ['NotaryDivision', 'OtherNotaryDivision']

NOTARY_GROUP = 'notaries'

NOTARY_LOCAL_GROUPS = (
    {'groupname': 'etude_leclercq', 'title': 'Étude du Notaire Damien LE CLERCQ'},
)

DGO4_GROUP = 'dgo4'

DGO4_LOCAL_GROUPS = (
    {'groupname': 'dgo4_brabant', 'title': 'Brabant'},
    {'groupname': 'dgo4_lux', 'title': 'Luxembourg'},
    {'groupname': 'dgo4_namur', 'title': 'Namur'},
    {'groupname': 'dgo4_liege_1', 'title': 'Liège 1'},
    {'groupname': 'dgo4_liege_2', 'title': 'Liège 2'},
    {'groupname': 'dgo4_liege_ger', 'title': 'Liège - Cellule germanophone'},
    {'groupname': 'dgo4_hainaut_1', 'title': 'Hainaut 1'},
    {'groupname': 'dgo4_hainaut_2', 'title': 'Hainaut 2'},
)

TOWNSHIP_GROUP = 'townships'

TOWNSHIPS_LOCAL_GROUPS = (
    {'groupname': 'ac_namur', 'title': 'Namur'},
    {'groupname': 'ac_sambreville', 'title': 'Sambreville'},
)

POD_TEMPLATES = (
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
)
