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
        ('File format', ['files.file_format']),
        ('File content', ['files.content_type']),
        ('Fileset accession', ['accession']),  # All file_set_type accessions
        ('Fileset Subtype', ['@type']),  # All file_set_type titles
        ('Fileset type', ['file_set_type']),  # All assay_types file_set_type
        ('Assay', ['assay_term.term_name']),  # MeasurementSet assay_term
        ('Preferred assay title', ['preferred_assay_title']),  # MeasurementSet preferred_assay_title
        ('Assay titles', ['assay_titles']),  # AnalysisSet assay_titles
        ('Auxiliary set assay', ['measurement_sets.preferred_assay_title']),  # AuxiliarySet preferred_assay_title
        ('Donor(s)', ['donors.accession']),  # MeasurementSet donors
        ('Sample(s)', ['samples.accession']),  # MeasurementSet samples
        ('Sample term name', ['samples.sample_terms.term_name']),  # MeasurementSet samples.sample_terms.term_name
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
