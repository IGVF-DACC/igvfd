from snovault import (
    collection,
    load_schema
)
from .base import (
    Item
)


@collection(
    name='workflows',
    unique_key='uuid',
    properties={
        'title': 'Workflow',
        'description': 'Listing of workflows',
    }
)
class Workflow(Item):
    item_type = 'workflow'
    schema = load_schema('igvfd:schemas/workflow.json')
    rev = {
        'analysis_steps': ('AnalysisStep', 'workflow')
    }

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
