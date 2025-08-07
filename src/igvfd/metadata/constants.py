from collections import OrderedDict


METADATA_ALLOWED_TYPES = [
    'FileSet',
    'MeasurementSet',
    'AnalysisSet',
    'AuxiliarySet',
    'ConstructLibrarySet',
    'CuratedSet',
    'ModelSet',
    'PredictionSet',
]


FILE_METADATA_ALLOWED_TYPES = [
    'File',
    'AlignmentFile',
    'ConfigurationFile',
    'ImageFile',
    'IndexFile',
    'MatrixFile',
    'ModelFile',
    'ReferenceFile',
    'SequenceFile',
    'SignalFile',
    'TabularFile',
]


METADATA_COLUMN_TO_FIELDS_MAPPING = OrderedDict(
    [
        ('File accession', ['files.accession']),
        ('File id', ['files.@id']),
        ('File format', ['files.file_format']),
        ('File content', ['files.content_type']),
        ('Fileset accession', ['accession']),
        ('Fileset classification', ['@type']),
        ('Fileset type', ['file_set_type']),
        ('Preferred assay titles', ['preferred_assay_titles']),
        ('Assay titles', ['assay_titles']),
        ('Donor(s)', ['donors.accession']),
        ('Sample(s)', ['samples.accession']),
        ('Sample term name', ['samples.sample_terms.term_name']),
        ('Creation timestamp', ['creation_timestamp']),
        ('File size', ['files.file_size']),
        ('Fileset lab', ['lab.title']),
        ('File download URL', ['files.href']),
        ('File s3_uri', ['files.s3_uri']),
        ('File assembly', ['files.assembly']),
        ('File transcriptome annotation', ['files.transcriptome_annotation']),
        ('File controlled access', ['files.controlled_access']),
        ('File md5sum', ['files.md5sum']),
        ('File derived from', ['files.derived_from']),
        ('File upload status', ['files.upload_status']),
    ]
)


METADATA_AUDIT_TO_AUDIT_COLUMN_MAPPING = [
    ('WARNING', 'Audit WARNING'),
    ('NOT_COMPLIANT', 'Audit NOT_COMPLIANT'),
    ('ERROR', 'Audit ERROR'),
]


BATCH_DOWNLOAD_COLUMN_TO_FIELDS_MAPPING = OrderedDict(
    [
        ('File download URL', ['files.href']),
    ]
)


METADATA_LINK = '"{}/metadata/?{}"'


AT_IDS_AS_JSON_DATA_LINK = (
    ' -X GET '
    '-H "Accept: text/tsv" '
    '-H "Content-Type: application/json" '
    '--data \'{{"elements": [{}]}}\''
)


BOOLEAN_MAP = {
    'true': True,
    'false': False
}


FROM_FILESET_FIELDS = OrderedDict(
    [
        ('File id', ['files.@id']),
        ('File download URL', ['files.href']),
        ('File accession', ['files.accession']),
        ('File format', ['files.file_format']),
        ('File type', ['files.file_format_type']),
        ('File content type', ['files.content_type']),
        ('File summary', ['files.summary']),
        ('Fileset accession', ['accession']),
        ('Fileset type', ['file_set_type']),
        ('Assay titles', ['assay_titles']),
        ('Preferred assay titles', ['preferred_assay_titles']),
        ('Donors', ['donors.@id']),
        ('Samples', ['samples.@id']),
        ('Sample term names', ['samples.sample_terms.term_name']),
        ('Sample summaries', ['samples.summary']),
        ('Cell type annotation', ['files.cell_type_annotation']),
        ('Creation timestamp', ['files.creation_timestamp']),
        ('File size', ['files.file_size']),
        ('Fileset lab', ['lab.title']),
        ('File s3_uri', ['files.s3_uri']),
        ('File assembly', ['files.assembly']),
        ('File transcriptome annotation', ['files.transcritome_annotation']),
        ('File controlled access', ['files.controlled_access']),
        ('File Anvil URL', ['files.anvil_url']),
        ('File md5sum', ['files.md5sum']),
        ('File derived from', ['files.derived_from']),
        ('File status', ['files.status']),
        ('File upload status', ['files.upload_status']),
        ('Flowcell ID', ['files.flowcell_id']),
        ('Lane', ['files.lane']),
        ('Sequencing Run', ['files.sequencing_run']),
        ('Illumina Read Type', ['files.illumina_read_type']),
        ('Mean Read Length', ['files.mean_read_length']),
        ('Seq Specs', ['files.seqspecs']),
        ('Seq Spec Document', ['files.seqspec_document.@id']),
        ('Sequencing Kit', ['files.sequencing_kit']),
        ('Sequencing Platform', ['files.sequencing_platform.term_name']),
        ('Workflows', ['files.workflows.accession']),
    ]
)


FROM_FILE_FIELDS = OrderedDict(
    [
        ('File id', ['@id']),
        ('File download URL', ['href']),
        ('File accession', ['accession']),
        ('File format', ['file_format']),
        ('File type', ['file_format_type']),
        ('File content type', ['content_type']),
        ('File summary', ['summary']),
        ('Fileset accession', ['file_set.accession']),
        ('Fileset type', ['file_set.file_set_type']),
        ('Assay titles', ['assay_titles']),
        ('Preferred assay titles', ['preferred_assay_titles']),
        ('Donors', ['file_set.donors.@id']),
        ('Samples', ['file_set.samples.@id']),
        ('Sample term names', ['file_set.samples.sample_terms.term_name']),
        ('Sample summaries', ['file_set.samples.summary']),
        ('Cell type annotation', ['cell_type_annotation.@id']),
        ('Creation timestamp', ['creation_timestamp']),
        ('File size', ['file_size']),
        ('Fileset lab', ['file_set.lab.title']),
        ('File s3_uri', ['s3_uri']),
        ('File assembly', ['assembly']),
        ('File transcriptome annotation', ['transcriptome_annotation']),
        ('File controlled access', ['controlled_access']),
        ('File Anvil URL', ['anvil_url']),
        ('File md5sum', ['md5sum']),
        ('File derived from', ['derived_from']),
        ('File status', ['status']),
        ('File upload status', ['upload_status']),
        ('Flowcell ID', ['flowcell_id']),
        ('Lane', ['lane']),
        ('Sequencing Run', ['sequencing_run']),
        ('Illumina Read Type', ['illumina_read_type']),
        ('Mean Read Length', ['mean_read_length']),
        ('Seq Specs', ['seqspecs']),
        ('Seq Spec Document', ['seqspec_document.@id']),
        ('Sequencing Kit', ['sequencing_kit']),
        ('Sequencing Platform', ['sequencing_platform.term_name']),
        ('Workflows', ['workflows.accession']),
    ]
)


RECURSE_FILE_SET_LINK_FIELDS = [
    'construct_library_sets',
    'control_file_sets',
    'measurement_sets',
    'control_for',
    'input_file_sets',
    'input_for',
    'auxiliary_sets',
    'related_multiome_datasets',
    'file_sets',
]


RECURSE_FILE_FIELDS = [
    'files',
    'integrated_content_files',
    'barcode_replacement_file',
    'large_scale_gene_list',
    'large_scale_loci_list',
    'barcode_map',
    'onlist_files',
]
