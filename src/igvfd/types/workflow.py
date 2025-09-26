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
        Path('award', include=['@id', 'component']),
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
