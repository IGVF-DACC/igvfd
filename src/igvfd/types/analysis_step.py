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
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('parents', include=['@id', 'title', 'status']),
        Path('workflow', include=['@id', 'accession', 'name', 'status']),
        Path('submitted_by', include=['@id', 'title']),
        Path('analysis_step_versions.software_versions', include=[
             '@id', 'analysis_step_versions', 'software_versions', 'name'])
    ]

    rev = {
        'analysis_step_versions': ('AnalysisStepVersion', 'analysis_step')
    }

    set_status_up = []
    set_status_down = []

    def unique_keys(self, properties):
        keys = super(AnalysisStep, self).unique_keys(properties)
        keys.setdefault('analysis_step:name', []).append(self._name(properties))
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
        workflow_uuid = properties['workflow']
        workflow = root.get_by_uuid(workflow_uuid)
        return u'{}-{}'.format(workflow.upgrade_properties()['accession'], properties['step_label'])

    @calculated_property(schema={
        'title': 'Analysis Step Versions',
        'description': 'The analysis step versions associated with this analysis step.',
        'type': 'array',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Analysis Step Version',
            'type': 'string',
            'linkFrom': 'AnalysisStepVersion.analysis_step',
        },
        'notSubmittable': True
    })
    def analysis_step_versions(self, request, analysis_step_versions):
        return paths_filtered_by_status(request, analysis_step_versions)
