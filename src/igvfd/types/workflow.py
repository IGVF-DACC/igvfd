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
    rev = {
        'analysis_steps': ('AnalysisStep', 'workflow')
    }
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('submitted_by', include=['@id', 'title']),
        Path('standards_page', include=['@id', 'title'])
    ]

    @calculated_property(schema={
        'title': 'Analysis Steps',
        'type': 'array',
        'items': {
            'type': ['string', 'object'],
            'linkFrom': 'AnalysisStep.workflow',
        },
        'notSubmittable': True
    })
    def analysis_steps(self, request, analysis_steps):
        return paths_filtered_by_status(request, analysis_steps)
