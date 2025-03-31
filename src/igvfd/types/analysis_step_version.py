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
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('analysis_step', include=['@id', 'name', 'status', 'title']),
        Path('software_versions', include=['@id', 'name', 'status']),
        Path('submitted_by', include=['@id', 'title']),
    ]

    set_status_up = ['software_versions']
    set_status_down = []
