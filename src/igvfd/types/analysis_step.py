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
    unique_key='analysis_step:uuid',
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
        Path('submitted_by', include=['@id', 'title']),
        Path(
            'analysis_step_versions',
            include=[
                '@id',
                'software_versions',
                'workflows',
            ]
        ),
        Path(
            'analysis_step_versions.software_versions',
            include=[
                '@id',
                'name',
                'status',
            ]
        ),
        Path(
            'analysis_step_versions.workflows',
            include=[
                '@id',
                'accession',
                'name',
                'status'
            ]
        ),
    ]

    rev = {
        'analysis_step_versions': ('AnalysisStepVersion', 'analysis_step')
    }

    set_status_up = []
    set_status_down = []

    @calculated_property(
        schema={
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
        }
    )
    def analysis_step_versions(self, request, analysis_step_versions):
        return paths_filtered_by_status(request, analysis_step_versions)
