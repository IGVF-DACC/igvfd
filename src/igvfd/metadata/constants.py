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
