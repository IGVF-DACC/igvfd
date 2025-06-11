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
    unique_key='analysis_step_version:uuid',
    properties={
        'title': 'Analysis Step Versions',
        'description': 'Listing of analysis step versions',
    }
)
class AnalysisStepVersion(Item):
    item_type = 'analysis_step_version'
    schema = load_schema('igvfd:schemas/analysis_step_version.json')
    rev = {
        'workflows': ('Workflow', 'analysis_step_versions')
    }
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('analysis_step', include=['@id', 'status', 'title',
             'analysis_step_types', 'output_content_types', 'input_content_types']),
        Path('software_versions', include=['@id', 'name', 'status']),
        Path('submitted_by', include=['@id', 'title'])
    ]

    set_status_up = ['software_versions']
    set_status_down = []

    @calculated_property(schema={
        'title': 'Workflows',
        'type': 'array',
        'description': 'The workflows that this analysis step version is a part of.',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Workflow',
            'type': 'string',
            'linkFrom': 'Workflow.analysis_step_versions'
        },
        'notSubmittable': True
    })
    def workflows(self, request, workflows):
        """Return the workflow that this analysis step version is linked to."""
        return paths_filtered_by_status(request, workflows)
