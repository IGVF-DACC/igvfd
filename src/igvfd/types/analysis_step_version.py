from snovault import (
    calculated_property,
    collection,
    load_schema,
)
from snovault.util import Path
from .base import (
    Item,
    paths_filtered_by_status
)
from pyramid.traversal import (
    find_root,
    resource_path
)


@collection(
    name='analysis-step-versions',
    unique_key='analysis_step_version:name',
    properties={
        'title': 'Analysis Step Versions',
        'description': 'Listing of analysis step versions',
    }
)
class AnalysisStepVersion(Item):
    item_type = 'analysis_step_version'
    schema = load_schema('igvfd:schemas/analysis_step_version.json')
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('analysis_step', include=['@id', 'name']),
        Path('software_versions', include=['@id', 'name']),
        Path('submitted_by', include=['@id', 'title']),
    ]

    set_status_up = ['software_versions']
    set_status_down = []

    def unique_keys(self, properties):
        keys = super(AnalysisStepVersion, self).unique_keys(properties)
        keys.setdefault('analysis_step_version:name', []).append(self._name(properties))
        return keys

    @calculated_property(schema={
        'title': 'Name',
        'type': 'string',
        'description': 'Full name of the analysis step.',
        'comment': 'Do not submit. Value is automatically assigned by the server.',
        'notSubmittable': True,
        'uniqueKey': True
    })
    def name(self):
        return self.__name__

    @property
    def __name__(self):
        properties = self.upgrade_properties()
        return self._name(properties)

    def _name(self, properties):
        root = find_root(self)
        analysis_step_uuid = properties['analysis_step']
        print(analysis_step.upgrade_properties())
        analysis_step = root.get_by_uuid(analysis_step_uuid)
        format_creation_timestamp = properties['creation_timestamp'][:10]
        return u'{}-{}'.format(analysis_step.upgrade_properties()['name'], format_creation_timestamp)
