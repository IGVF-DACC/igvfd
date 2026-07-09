from snovault import (
    calculated_property,
    collection,
    load_schema
)
from snovault.util import Path
from .base import (
    Item,
    paths_filtered_by_status
)
from .file_set import get_preferred_assay_slims


@collection(
    name='workflows',
    unique_key='accession',
    properties={
        'title': 'Workflows',
        'description': 'Listing of workflows',
    }
)
class Workflow(Item):
    item_type = 'workflow'
    name_key = 'accession'
    schema = load_schema('igvfd:schemas/workflow.json')

    embedded_with_frame = [
        Path('award', include=['@id', 'component', 'project']),
        Path('lab', include=['@id', 'title']),
        Path('submitted_by', include=['@id', 'title']),
        Path('standards_page', include=['@id', 'title', 'status']),
        Path('publications', include=['@id', 'publication_identifiers', 'status']),
        Path(
            'analysis_step_versions',
            include=[
                '@id',
                'status',
                'software_versions',
                'analysis_step',
            ]
        ),
        Path(
            'analysis_step_versions.analysis_step',
            include=[
                '@id',
                'title',
                'status',
                'analysis_step_types',
                'input_content_types',
                'output_content_types',
            ]
        ),
        Path(
            'analysis_step_versions.software_versions',
            include=[
                '@id',
                'name',
                'software',
            ],
        ),
        Path(
            'analysis_step_versions.software_versions.software',
            include=[
                '@id',
                'title',
                'name',
                'status',
            ]
        ),
    ]

    set_status_up = [
        'documents',
        'standards_page'
    ]
    set_status_down = []

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, name, workflow_version=None):
        summary_parts = [
            name,
            workflow_version
        ]
        return ' '.join([x for x in summary_parts if x is not None])

    @calculated_property(
        schema={
            'title': 'Preferred Assay Slims',
            'description': 'Preferred Assay Slim(s) of assays that produced data analyzed in the analysis set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Preferred Assay Slim',
                'description': 'Category of assay that produced data analyzed in the analysis set.',
                'type': 'string'
            },
            'notSubmittable': True,
        }
    )
    def preferred_assay_slims(self, request, preferred_assay_titles=None):
        return get_preferred_assay_slims(preferred_assay_titles)
