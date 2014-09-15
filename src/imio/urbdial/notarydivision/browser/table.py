## -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.browser.interfaces import ICreatedParcellingTable
from imio.urbdial.notarydivision.browser.interfaces import IEditableParcellingTable
from imio.urbdial.notarydivision.browser.interfaces import IParcellingTable
from imio.urbdial.notarydivision.content.vocabulary import DeedTypesVocabularyFactory
from imio.urbdial.notarydivision.content.vocabulary import LocalitiesVocabularyFactory
from imio.urbdial.notarydivision.content.vocabulary import SurfaceAccuraciesVocabularyFactory
from imio.urbdial.notarydivision.utils import translate

from z3c.table.column import Column
from z3c.table.table import Table
from z3c.table.value import ValuesMixin

from zope.interface import implements


class ParcellingTable(Table):
    """
    """
    implements(IParcellingTable)


class CreatedParcellingTable(ParcellingTable):
    """
    """
    implements(ICreatedParcellingTable)

    cssClasses = {'table': 'listing largetable'}


class EditableCreatedParcellingTable(CreatedParcellingTable):
    """
    """
    implements(IEditableParcellingTable)


class CreatedParcellingValues(ValuesMixin):
    """
    """
    @property
    def values(self):
        notarydivision = self.context
        created_parcellings = notarydivision.get_parcellings(portal_type='CreatedParcelling')
        return created_parcellings


class UrbdialColumn(Column):
    """
    """

    def renderHeadCell(self):
        """Header cell content."""
        return translate(self.header)

    def get(self, obj, attr):
        val = getattr(obj, attr)
        if val is None:
            val = ''
        if val is True:
            val = translate('True')
        if val is False:
            val = translate('False')
        return val


class ParcellingNumberColumn(UrbdialColumn):
    """
    """

    header = 'label_colname_number'
    weight = 10

    def renderCell(self, parcelling):
        number = self.get(parcelling, 'number')
        return number


class LocalisationColumn(UrbdialColumn):
    """
    """

    header = 'Parcelling localisation'
    weight = 20

    def renderCell(self, parcelling):
        localisation = self.get(parcelling, 'localisation')
        if localisation:
            localisation_voc_factory = LocalitiesVocabularyFactory()
            localisation_voc = localisation_voc_factory(parcelling)
            localisation = localisation_voc.getTerm(localisation).title
        return localisation


class SurfaceColumn(UrbdialColumn):
    """
    """

    header = 'Surface'
    weight = 40

    def renderCell(self, parcelling):
        surface = self.get(parcelling, 'surface')
        return surface


class SurfaceAccuracyColumn(UrbdialColumn):
    """
    """

    header = 'Surface'
    weight = 40

    def renderCell(self, parcelling):
        surface = self.get(parcelling, 'surface')
        if surface:
            accuracy = self.get(parcelling, 'surface_accuracy')
            accuracy_voc_factory = SurfaceAccuraciesVocabularyFactory()
            accuracy_voc = accuracy_voc_factory(parcelling)
            accuracy = accuracy_voc.getTerm(accuracy).title
            surface = surface and u'{} ({})'.format(surface, accuracy) or ''
        return surface


class RoadDistanceColumn(UrbdialColumn):
    """
    """

    header = 'Road distance'
    weight = 50

    def renderCell(self, parcelling):
        road_distance = self.get(parcelling, 'road_distance')
        if road_distance:
            road_distance = u'{} m'.format(road_distance)
        return road_distance


class DestinationColumn(UrbdialColumn):
    """
    """

    header = 'Parcelling destination'
    weight = 60

    def renderCell(self, parcelling):
        destination = self.get(parcelling, 'destination')
        return destination


class CededColumn(UrbdialColumn):
    """
    """

    header = 'Ceded parcelling'
    weight = 65

    def renderCell(self, parcelling):
        ceded = parcelling.ceded_parcelling and 'Yes' or 'No'
        ceded_display = translate(ceded, domain='plone')
        return  ceded_display


class DeedTypeColumn(UrbdialColumn):
    """
    """

    header = 'Deed type'
    weight = 70

    def renderCell(self, parcelling):
        if not parcelling.ceded_parcelling:
            return u'/'

        deed_type = self.get(parcelling, 'deed_type')
        if deed_type == 'autre':
            deed_type = self.get(parcelling, 'other_deed_type')
        elif deed_type:
            deed_type_voc_factory = DeedTypesVocabularyFactory()
            deed_type_voc = deed_type_voc_factory(parcelling)
            deed_type = deed_type_voc.getTerm(deed_type).title
        return deed_type


class BuiltColumn(UrbdialColumn):
    """
    """

    header = 'Built'
    weight = 80

    def renderCell(self, parcelling):
        built = self.get(parcelling, 'built')
        return built


class UndividedColumn(UrbdialColumn):
    """
    """

    header = 'Undivided or dismemberment'
    weight = 90
    undivided = 'undivided'

    def renderCell(self, parcelling):
        undivided = getattr(parcelling, self.undivided)
        if undivided:
            undivided = self.get(parcelling, self.undivided)
            specific_rights = translate('Specific rights')
            link = '<a class="link-overlay" href="{ref}/@@specificrights">{rights}</a>'.format(
                ref=parcelling.absolute_url(),
                rights=specific_rights
            )
            undivided = '<span id="urbdial-undivided">{undivided}.&nbsp&nbsp&nbsp{link}</span>'.format(
                undivided=undivided,
                link=link
            )
        else:
            undivided = self.get(parcelling, self.undivided)
        return undivided


class ActionsColumn(UrbdialColumn):
    """
    """

    weight = 100
    cssClasses = {'th': 'actionsheader'}
    header = 'actions'

    def renderCell(self, parcelling):
        actions = parcelling.restrictedTraverse('actions_panel')
        return actions()
