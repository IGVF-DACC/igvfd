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
        Path('analysis_step_versions.software_versions.software',
             include=['@id', 'title', 'name', 'software_versions', 'software', 'status']),
        Path('analysis_step_versions.analysis_step',
             include=['@id', 'title', 'analysis_step_types', 'output_content_types', 'input_content_types', 'status', 'analysis_step']),
        Path('analysis_steps', include=['@id', 'title', 'analysis_step_types',
             'output_content_types', 'input_content_types', 'status'])
    ]
    rev_link = {
        'analysis_step_versions': ('AnalysisStepVersion', 'workflow')
    }

    set_status_up = [
        'analysis_step_versions',
        'standards_page'
    ]
    set_status_down = []

    @calculated_property(
        define=True,
        schema={
            'title': 'Analysis Steps',
            'description': 'The analysis steps associated with this workflow.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Analysis Step',
                'type': ['string', 'object'],
                'linkFrom': 'AnalysisStepVersion.workflows'
            },
            'notSubmittable': True
        })
    def analysis_steps(self, request, analysis_step_versions=[]):
        """
        Returns the analysis step versions associated with this workflow, filtered by status.
        """
        analysis_steps = set()
        for asv in analysis_step_versions:
            asv_obj = request.embed(asv, '@@object?skip_calculated=true')
            as_obj = request.embed(asv_obj['analysis_step'], '@@object')
            analysis_steps.add(as_obj['@id'])
        return paths_filtered_by_status(request, sorted(analysis_steps))
