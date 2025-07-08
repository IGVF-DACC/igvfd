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


METADATA_COLUMN_TO_FIELDS_MAPPING = OrderedDict(
    [
        ('File accession', ['files.accession']),
        ('File id', ['files.@id']),
        ('File format', ['files.file_format']),
        ('File format type', ['files.file_format_type']),
        ('File content type', ['files.content_type']),
        ('File summary', ['files.summary']),
        ('Fileset accession', ['files.file_set.accession']),
        ('Fileset type', ['files.file_set.file_set_type']),
        ('Preferred assay titles', ['files.preferred_assay_titles']),
        ('Assay titles', ['files.assay_titles']),
        ('Donor(s)', ['files.file_set.donors.accession']),
        ('Sample(s)', ['files.file_set.samples.accession']),
        ('Sample term name', ['files.file_set.samples.sample_terms.term_name']),
        ('Creation timestamp', ['files.creation_timestamp']),
        ('File size', ['files.file_size']),
        ('Fileset lab', ['files.file_set.lab.title']),
        ('File download URL', ['files.href']),
        ('File s3_uri', ['files.s3_uri']),
        ('File assembly', ['files.assembly']),
        ('File transcriptome annotation', ['files.transcriptome_annotation']),
        ('File controlled access', ['files.controlled_access']),
        ('File anvil_url', ['files.anvil_url']),
        ('File md5sum', ['files.md5sum']),
        ('File derived from', ['files.derived_from']),
        ('File upload status', ['files.upload_status']),
        ('File cell type annotation', ['files.cell_type_annotation']),
        ('File sequencing run', ['files.sequencing_run']),
        ('File flowcell ID', ['files.flowcell_id']),
        ('File lane', ['files.lane']),
        ('File read names', ['files.read_names']),
        ('File mean read length', ['files.mean_read_length']),
        ('File seqspecs', ['files.seqspecs']),
        ('File seqspec document', ['files.seqspec_document']),
        ('File sequencing kit', ['files.sequencing_kit']),
        ('File sequencing platform', ['files.sequencing_platform']),
        ('File workflow name', ['files.workflow.name'])
    ]
)


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
