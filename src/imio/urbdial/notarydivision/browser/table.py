## -*- coding: utf-8 -*-

from imio.urbdial.notarydivision.browser.interfaces import ICreatedParcelTable
from imio.urbdial.notarydivision.browser.interfaces import IEditableParcelTable
from imio.urbdial.notarydivision.browser.interfaces import IInitialParcelTable
from imio.urbdial.notarydivision.browser.interfaces import INextParcelsTable
from imio.urbdial.notarydivision.browser.interfaces import IParcelTable
from imio.urbdial.notarydivision.browser.interfaces import IPreviouParcelsTable
from imio.urbdial.notarydivision.content.vocabulary import DeedTypesVocabularyFactory
from imio.urbdial.notarydivision.content.vocabulary import LocalitiesVocabularyFactory
from imio.urbdial.notarydivision.content.vocabulary import SurfaceAccuraciesVocabularyFactory
from imio.urbdial.notarydivision.utils import translate

from z3c.table.column import Column
from z3c.table.table import Table
from z3c.table.value import ValuesMixin

from zope.interface import implements


class ParcelTable(Table):
    """
    """
    implements(IParcelTable)


class InitialParcelTable(Table):
    """
    """
    implements(IInitialParcelTable)

    cssClasses = {'table': 'listing largetable'}


class CreatedParcelTable(Table):
    """
    """
    implements(ICreatedParcelTable)

    cssClasses = {'table': 'listing largetable'}


class EditableInitialParcelTable(InitialParcelTable):
    """
    """
    implements(IEditableParcelTable)


class EditableCreatedParcelTable(CreatedParcelTable):
    """
    """
    implements(IEditableParcelTable)


class PreviousInitialParcelsTable(InitialParcelTable):
    """
    """
    implements(IPreviouParcelsTable)


class NextInitialParcelsTable(InitialParcelTable):
    """
    """
    implements(INextParcelsTable)


class PreviousCreatedParcelsTable(InitialParcelTable):
    """
    """
    implements(IPreviouParcelsTable)


class NextCreatedParcelsTable(InitialParcelTable):
    """
    """
    implements(INextParcelsTable)


class InitialParcelValues(ValuesMixin):
    """
    """
    @property
    def values(self):
        notarydivision = self.context
        initial_parcels = notarydivision.get_parcels(portal_type='InitialParcel')
        return initial_parcels


class CreatedParcelValues(ValuesMixin):
    """
    """
    @property
    def values(self):
        notarydivision = self.context
        created_parcels = notarydivision.get_parcels(portal_type='CreatedParcel')
        return created_parcels


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


class ParcelNumberColumn(UrbdialColumn):
    """
    """

    header = 'label_colname_number'
    weight = 10

    def renderCell(self, parcel):
        number = self.get(parcel, 'number')
        return number


class LocalityColumn(UrbdialColumn):
    """
    """

    header = 'Locality'
    weight = 20

    def renderCell(self, parcel):
        locality = self.get(parcel, 'locality')
        if locality:
            locality_voc_factory = LocalitiesVocabularyFactory()
            locality_voc = locality_voc_factory(parcel)
            locality = locality_voc.getTerm(locality).title
        return locality


class CadastralReferenceColumn(UrbdialColumn):
    """
    """

    header = 'label_colname_cadastral_ref'
    weight = 30

    def renderCell(self, parcel):
        division = self.get(parcel, 'division')
        section = self.get(parcel, 'section')
        radical = self.get(parcel, 'radical')
        bis = self.get(parcel, 'bis')
        exposant = self.get(parcel, 'exposant')
        power = self.get(parcel, 'power')

        reference = '{division} {section} {radical}{bis} {exposant} {power}'.format(
            division=division,
            section=section,
            radical=radical,
            bis=bis and '/{}'.format(bis) or '',
            exposant=exposant,
            power=power
        )
        return reference


class AddressColumn(UrbdialColumn):
    """
    """

    header = 'Street'
    weight = 35

    def renderCell(self, parcel):
        street = self.get(parcel, 'street')
        street_number = self.get(parcel, 'street_number')
        if street:
            if street_number:
                address = u'{}, {}'.format(street_number, street)
            else:
                address = street
        else:
            address = street_number
        return address


class SurfaceColumn(UrbdialColumn):
    """
    """

    header = 'Surface'
    weight = 40

    def renderCell(self, parcel):
        surface = self.get(parcel, 'surface')
        return surface


class SurfaceAccuracyColumn(UrbdialColumn):
    """
    """

    header = 'Surface'
    weight = 40

    def renderCell(self, parcel):
        surface = self.get(parcel, 'surface')
        if surface:
            accuracy = self.get(parcel, 'surface_accuracy')
            accuracy_voc_factory = SurfaceAccuraciesVocabularyFactory()
            accuracy_voc = accuracy_voc_factory(parcel)
            accuracy = accuracy_voc.getTerm(accuracy).title
            surface = surface and u'{} ({})'.format(surface, accuracy) or ''
        return surface


class ActualUseColumn(UrbdialColumn):
    """
    """

    header = 'Estate actual use'
    weight = 50

    def renderCell(self, parcel):
        actual_use = self.get(parcel, 'actual_use')
        return actual_use


class RoadDistanceColumn(UrbdialColumn):
    """
    """

    header = 'Road distance'
    weight = 50

    def renderCell(self, parcel):
        road_distance = self.get(parcel, 'road_distance')
        if road_distance:
            road_distance = u'{} m'.format(road_distance)
        return road_distance


class DeedTypeColumn(UrbdialColumn):
    """
    """

    header = 'Deed type'
    weight = 60

    def renderCell(self, parcel):
        deed_type = self.get(parcel, 'deed_type')
        if deed_type == 'autre':
            deed_type = self.get(parcel, 'other_deed_type')
        elif deed_type:
            deed_type_voc_factory = DeedTypesVocabularyFactory()
            deed_type_voc = deed_type_voc_factory(parcel)
            deed_type = deed_type_voc.getTerm(deed_type).title
        return deed_type


class DestinationColumn(UrbdialColumn):
    """
    """

    header = 'Parcel destination'
    weight = 70

    def renderCell(self, parcel):
        destination = self.get(parcel, 'destination')
        return destination


class BuiltColumn(UrbdialColumn):
    """
    """

    header = 'Built'
    weight = 80

    def renderCell(self, parcel):
        built = self.get(parcel, 'built')
        return built


class UndividedColumn(UrbdialColumn):
    """
    """

    header = 'Undivided or dismemberment'
    undivided = 'undivided_b'

    def renderCell(self, parcel):
        undivided = getattr(parcel, self.undivided)
        if undivided:
            undivided = self.get(parcel, self.undivided)
            specific_rights = translate('Specific rights')
            link = '<a class="link-overlay" href="{ref}/@@specificrights">{rights}</a>'.format(
                ref=parcel.absolute_url(),
                rights=specific_rights
            )
            undivided = '<span id="urbdial-undivided">{undivided}.&nbsp&nbsp&nbsp{link}</span>'.format(
                undivided=undivided,
                link=link
            )
        else:
            undivided = self.get(parcel, self.undivided)
        return undivided


class InitialParcelUndividedColumn(UndividedColumn):
    """
    """

    weight = 60
    undivided = 'undivided_a'


class CreatedParcelUndividedColumn(UndividedColumn):
    """
    """

    weight = 90
    undivided = 'undivided_b'


class ActionsColumn(UrbdialColumn):
    """
    """

    weight = 100
    cssClasses = {'th': 'actionsheader'}
    header = 'actions'

    def renderCell(self, parcel):
        actions = parcel.restrictedTraverse('actions_panel')
        return actions()
