from snovault import (
    abstract_collection,
    calculated_property,
    collection,
    load_schema,
)

from .base import (
    Item,
)


@abstract_collection(
    name='files',
    unique_key='accession',
    properties={
        'title': 'Files',
        'description': 'Listing of files',
    })
class File(Item):
    item_type = 'file'
    base_types = ['File'] + Item.base_types
    name_key = 'accession'
    schema = load_schema('igvfd:schemas/file.json')


@collection(
    name='sequence-data',
    unique_key='accession',
    properties={
        'title': 'Sequence data',
        'description': 'Listing of sequence data files',
    })
class SequenceData(File):
    item_type = 'sequence_data'
    schema = load_schema('igvfd:schemas/sequence_data.json')

    def unique_keys(self, properties):
        keys = super(File, self).unique_keys(properties)
        if properties.get('status') != 'replaced':
            if 'md5sum' in properties:
                value = 'md5:{md5sum}'.format(**properties)
                keys.setdefault('alias', []).append(value)
        return keys


@collection(
    name='reference-data',
    unique_key='accession',
    properties={
        'title': 'Reference data',
        'description': 'Listing of reference data files',
    })
class ReferenceData(File):
    item_type = 'reference_data'
    schema = load_schema('igvfd:schemas/reference_data.json')

    def unique_keys(self, properties):
        keys = super(File, self).unique_keys(properties)
        if properties.get('status') != 'replaced':
            if 'md5sum' in properties:
                value = 'md5:{md5sum}'.format(**properties)
                keys.setdefault('alias', []).append(value)
        return keys


@collection(
    name='imaging-data',
    unique_key='accession',
    properties={
        'title': 'Imaging data',
        'description': 'Listing of imaging data files',
    })
class ImagingData(File):
    item_type = 'imaging_data'
    schema = load_schema('igvfd:schemas/imaging_data.json')

    def unique_keys(self, properties):
        keys = super(File, self).unique_keys(properties)
        if properties.get('status') != 'replaced':
            if 'md5sum' in properties:
                value = 'md5:{md5sum}'.format(**properties)
                keys.setdefault('alias', []).append(value)
        return keys
