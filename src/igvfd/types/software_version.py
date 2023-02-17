from snovault import (
    calculated_property,
    collection,
    load_schema
)
from snovault.util import Path
from .base import (
    Item
)
from pyramid.traversal import (
    find_root,
    resource_path
)


@collection(
    name='software-versions',
    unique_key='software_version:name',
    properties={
        'title': 'Software Version',
        'description': 'Software version pages',
    }
)
class SoftwareVersion(Item):
    item_type = 'software_version'
    schema = load_schema('igvfd:schemas/software_version.json')
    embedded_with_frame = [
        Path('award', include=['@id', 'component', 'name']),
        Path('lab', include=['@id', 'title']),
    ]

    def unique_keys(self, properties):
        keys = super(SoftwareVersion, self).unique_keys(properties)
        keys.setdefault('software_version:name', []).append(self._name(properties))
        return keys

    @calculated_property(schema={
        'title': 'Name',
        'type': 'string',
        'notSubmittable': True,
    })
    def name(self):
        return self.__name__

    @property
    def __name__(self):
        properties = self.upgrade_properties()
        return self._name(properties)

    def software_uuid(self, properties=None, return_uuid=False):
        if properties is None:
            properties = self.upgrade_properties()
        root = find_root(self)
        if 'software' in properties:
            software = properties['software']
        else:
            return None
        if return_uuid:
            return resource_path(root.get_by_uuid(software), '')

    def _name(self, properties):
        root = find_root(self)
        software_uuid = properties['software']
        software = root.get_by_uuid(software_uuid)
        source = software.upgrade_properties()['name']
        return u'{}-v{}'.format(source, properties['version'])

    def __resource_url__(self, request, info):
        request._linked_uuids.add(str(self.uuid))
        # Record software uuid in linked_uuids so linking objects record
        # the rename dependency.
        software_uuid = self.software_uuid(return_uuid=True)
        if software_uuid:
            request._linked_uuids.add(str(software_uuid))
        return None
