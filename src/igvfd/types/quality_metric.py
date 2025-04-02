from snovault.attachment import ItemWithAttachment
from snovault import (
    abstract_collection,
    calculated_property,
    collection,
    load_schema,
)
from snovault.util import Path
from .base import (
    Item,
    paths_filtered_by_status
)


@abstract_collection(
    name='quality-metrics',
    properties={
        'title': 'Quality Metrics',
        'description': 'Listing of quality metrics',
    }
)
class QualityMetric(Item, ItemWithAttachment):
    base_types = ['QualityMetric'] + Item.base_types
    item_type = 'quality_metric'
    schema = load_schema('igvfd:schemas/quality_metric.json')
    rev = {}
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('submitted_by', include=['@id', 'title']),
    ]
    audit_inherit = []
    set_status_up = []
    set_status_down = []

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'description': 'A summary of the quality metric.',
            'notSubmittable': True,
        }
    )
    def summary(self, quality_metric_of):
        return f'Quality metric of {", ".join(quality_metric_of)}'


@collection(
    name='single-cell-rna-seq-quality-metrics',
    properties={
        'title': 'Single Cell RNA-seq Quality Metrics',
        'description': 'Listing of single cell RNA-seq quality metrics',
    }
)
class SingleCellRnaSeqQualityMetric(QualityMetric):
    item_type = 'single_cell_rna_seq_quality_metric'
    schema = load_schema('igvfd:schemas/single_cell_rna_seq_quality_metric.json')
    embedded_with_frame = QualityMetric.embedded_with_frame + []
    audit_inherit = QualityMetric.audit_inherit
    set_status_up = QualityMetric.set_status_up + []
    set_status_down = QualityMetric.set_status_down + []


@collection(
    name='single-cell-atac-seq-quality-metrics',
    properties={
        'title': 'Single Cell ATAC-seq Quality Metrics',
        'description': 'Listing of single cell ATAC-seq quality metrics',
    }
)
class SingleCellAtacSeqQualityMetric(QualityMetric):
    item_type = 'single_cell_atac_seq_quality_metric'
    schema = load_schema('igvfd:schemas/single_cell_atac_seq_quality_metric.json')
    embedded_with_frame = QualityMetric.embedded_with_frame + []
    audit_inherit = QualityMetric.audit_inherit
    set_status_up = QualityMetric.set_status_up + []
    set_status_down = QualityMetric.set_status_down + []


@collection(
    name='mpra-quality-metrics',
    properties={
        'title': 'MPRA Quality Metrics',
        'description': 'Listing of MPRA quality metrics',
    }
)
class MpraQualityMetric(QualityMetric):
    item_type = 'mpra_quality_metric'
    schema = load_schema('igvfd:schemas/mpra_quality_metric.json')
    embedded_with_frame = QualityMetric.embedded_with_frame + []
    audit_inherit = QualityMetric.audit_inherit
    set_status_up = QualityMetric.set_status_up + []
    set_status_down = QualityMetric.set_status_down + []


@collection(
    name='starr-seq-quality-metrics',
    properties={
        'title': 'STARR-seq Quality Metrics',
        'description': 'Listing of STARR-seq quality metrics',
    }
)
class StarrSeqQualityMetric(QualityMetric):
    item_type = 'starr_seq_quality_metric'
    schema = load_schema('igvfd:schemas/starr_seq_quality_metric.json')
    embedded_with_frame = QualityMetric.embedded_with_frame + []
    audit_inherit = QualityMetric.audit_inherit
    set_status_up = QualityMetric.set_status_up + []
    set_status_down = QualityMetric.set_status_down + []


@collection(
    name='perturb-seq-quality-metrics',
    properties={
        'title': 'Perturb-seq Quality Metrics',
        'description': 'Listing of Perturb-seq quality metrics',
    }
)
class PerturbSeqQualityMetric(QualityMetric):
    item_type = 'perturb_seq_quality_metric'
    schema = load_schema('igvfd:schemas/perturb_seq_quality_metric.json')
    embedded_with_frame = QualityMetric.embedded_with_frame + []
    audit_inherit = QualityMetric.audit_inherit
    set_status_up = QualityMetric.set_status_up + []
    set_status_down = QualityMetric.set_status_down + []
