from collections import OrderedDict


METADATA_ALLOWED_TYPES = [
    'MeasurementSet',
]


METADATA_COLUMN_TO_FIELDS_MAPPING = OrderedDict(
    [
        ('File accession', ['files.accession']),
        ('File format', ['files.file_format']),
        ('File content', ['files.content_type']),
        ('File set', ['files.file_set']),
        ('Accession', ['accession']),
        ('Assay', ['assay_term.term_name']),
        ('Donor(s)', ['donors.accession']),
        ('Sample(s)', ['samples.accession']),
        ('Creation timestampe', ['creation_timestamp']),
        ('Size', ['files.file_size']),
        ('Lab', ['files.lab.title']),
        ('md5sum', ['files.md5sum']),
        ('File download URL', ['files.href']),
        ('File Status', ['files.status']),
        ('s3_uri', ['files.s3_uri']),
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
