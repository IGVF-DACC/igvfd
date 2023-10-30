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
    name='analysis-steps',
    unique_key='analysis_step:name',
    properties={
        'title': 'Analysis Steps',
        'description': 'Listing of analysis steps',
    }
)
class AnalysisStep(Item):
    item_type = 'analysis_step'
    schema = load_schema('igvfd:schemas/analysis_step.json')
    embedded_with_frame = [
        Path('lab', include=['@id', 'title']),
        Path('parents', include=['@id', 'title']),
        Path('workflow', include=['@id', 'accession'])
    ]

    def unique_keys(self, properties):
        keys = super(AnalysisStep, self).unique_keys(properties)
        keys.setdefault('analysis_step:name', []).append(self._name(properties))
        return keys

    @calculated_property(schema={
        'title': 'Name',
        'type': 'string',
        'description': 'Full name of the analysis step.',
        'comment': 'Do not submit. Value is automatically assigned by the server.',
        'uniqueKey': 'name'
    })
    def name(self):
        return self.__name__

    @property
    def __name__(self):
        properties = self.upgrade_properties()
        return self._name(properties)

    def _name(self, properties):
        root = find_root(self)
        workflow_uuid = properties['workflow']
        workflow = root.get_by_uuid(workflow_uuid)
        return u'{}-{}'.format(workflow.upgrade_properties()['accession'], properties['step_label'])
