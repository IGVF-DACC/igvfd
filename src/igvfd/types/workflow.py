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
        'analysis_step_versions': ('AnalysisStepVersion', 'workflow')
    }
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('submitted_by', include=['@id', 'title']),
        Path('standards_page', include=['@id', 'title', 'status']),
        Path('publications', include=['@id', 'publication_identifiers', 'status']),
        Path('analysis_steps.analysis_step_versions.software_versions.software',
             include=['@id', 'title', 'name', 'analysis_step_types', 'output_content_types', 'input_content_types', 'analysis_step_versions', 'software_versions', 'software', 'status'])
    ]

    set_status_up = [
        'analysis_steps',
        'standards_page'
    ]
    set_status_down = []

    @calculated_property(schema={
        'title': 'Analysis Steps',
        'type': 'array',
        'description': 'The analysis steps which are part of this workflow.',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Analysis Step',
            'type': ['string', 'object'],
            'linkTo': 'AnalysisStepVersion.analysis_step',
        },
        'notSubmittable': True
    })
    def analysis_steps(self, request, analysis_step_versions):
        analysis_steps = set()
        for asv in analysis_step_versions:
            # Analysis Step is a submitted property
            asv_obj = request.embed(asv, '@@object?skip_calculated=true')
            if asv_obj.get('analysis_step'):
                analysis_steps.add(asv_obj['analysis_step'])
        return paths_filtered_by_status(request, sorted(analysis_steps))
