import datetime
import os
import pytz
import time

from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPNotFound
from pyramid.httpexceptions import HTTPTemporaryRedirect

from pyramid.settings import asbool

from pyramid.view import view_config

from urllib.parse import parse_qs
from urllib.parse import urlparse

from snovault import abstract_collection
from snovault import calculated_property
from snovault import collection
from snovault import load_schema
from snovault import AfterModified
from snovault import BeforeModified

from snovault.attachment import InternalRedirect

from snovault.schema_utils import schema_validator

from snovault.util import Path

from igvfd.types.base import (
    Item,
    paths_filtered_by_status
)

from igvfd.upload_credentials import get_s3_client
from igvfd.upload_credentials import get_sts_client
from igvfd.upload_credentials import get_restricted_sts_client
from igvfd.upload_credentials import UploadCredentials


FILE_FORMAT_TO_FILE_EXTENSION = {
    'bam': '.bam',
    'bed': '.bed.gz',
    'bedpe': '.bedpe.gz',
    'bigBed': '.bigBed',
    'bigInteract': '.bigInteract',
    'bigWig': '.bigWig',
    'csv': '.csv.gz',
    'database': '.db',
    'dat': '.dat.gz',
    'fasta': '.fasta.gz',
    'fastq': '.fastq.gz',
    'gaf': '.gaf.gz',
    'gds': '.gds.gz',
    'gff': '.gff.gz',
    'gtf': '.gtf.gz',
    'idx': '.idx',
    'hic': '.hic',
    'h5ad': '.h5ad',
    'hdf5': '.h5',
    'idat': '.idat',
    'jpg': '.jpg',
    'json': '.json',
    'mtx': '.mtx',
    'obo': '.obo.gz',
    'owl': '.owl.gz',
    'pairs': '.pairs.gz',
    'pod5': '.pod5',
    'png': '.png',
    'PWM': '.pwm',
    'sam': '.sam.gz',
    'sra': '.sra',
    'tabix': '.tabix',
    'tagAlign': '.tagAlign.gz',
    'tar': '.tar.gz',
    'tsv': '.tsv.gz',
    'txt': '.txt.gz',
    'vcf': '.vcf.gz',
    'xml': '.xml.gz',
    'yaml': '.yaml.gz'
}


def show_upload_credentials(request=None, context=None, upload_status=None):
    if request is None or upload_status == 'validated':
        return False
    return request.has_permission('edit', context)


def show_href(anvil_url=None):
    return anvil_url is None


def show_s3uri(anvil_url=None):
    return anvil_url is None


@abstract_collection(
    name='files',
    unique_key='accession',
    properties={
        'title': 'Files',
        'description': 'Listing of files',
    }
)
class File(Item):
    item_type = 'file'
    base_types = ['File'] + Item.base_types
    name_key = 'accession'
    schema = load_schema('igvfd:schemas/file.json')
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('submitted_by', include=['@id', 'title']),
    ]
    rev = {
        'integrated_in': ('ConstructLibrarySet', 'integrated_content_files'),
        'gene_list_for': ('FileSet', 'large_scale_gene_list'),
        'loci_list_for': ('FileSet', 'large_scale_loci_list'),
        'input_file_for': ('File', 'derived_from')
    }

    set_status_up = [
        'file_format_specifications'
    ]
    set_status_down = []

    @calculated_property(schema={
        'title': 'Integrated In',
        'description': 'Construct library set(s) that this file was used for in insert design.',
        'type': 'array',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Integrated In',
            'type': ['string', 'object'],
            'linkFrom': 'ConstructLibrarySet.integrated_content_files',
        },
        'notSubmittable': True
    })
    def integrated_in(self, request, integrated_in):
        return paths_filtered_by_status(request, integrated_in)

    @calculated_property(schema={
        'title': 'Input File For',
        'description': 'The files which have been used for deriving this file as an input.',
        'type': 'array',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Input File For',
            'type': ['string', 'object'],
            'linkFrom': 'File.derived_from',
        },
        'notSubmittable': True
    })
    def input_file_for(self, request, input_file_for):
        return paths_filtered_by_status(request, input_file_for)

    @calculated_property(schema={
        'title': 'Gene List For',
        'description': 'File Set(s) that this file is a gene list for.',
        'type': 'array',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Gene List For',
            'type': ['string', 'object'],
            'linkFrom': 'FileSet.large_scale_gene_list',
        },
        'notSubmittable': True
    })
    def gene_list_for(self, request, gene_list_for):
        return paths_filtered_by_status(request, gene_list_for)

    @calculated_property(schema={
        'title': 'Loci List For',
        'description': 'File Set(s) that this file is a loci list for.',
        'type': 'array',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Loci List For',
            'type': ['string', 'object'],
            'linkFrom': 'FileSet.large_scale_loci_list',
        },
        'notSubmittable': True
    })
    def loci_list_for(self, request, loci_list_for):
        return paths_filtered_by_status(request, loci_list_for)

    @calculated_property(
        condition=show_href,
        schema={
            'title': 'Download URL',
            'description': 'The download path to obtain file.',
            'comment': 'Do not submit. This is issued by the server.',
            'type': 'string',
        }
    )
    def href(self, request, file_format, accession):
        file_extension = FILE_FORMAT_TO_FILE_EXTENSION[file_format]
        filename = f'{accession}{file_extension}'
        return request.resource_path(
            self,
            '@@download',
            filename
        )

    @calculated_property(
        condition=show_s3uri,
        schema={
            'title': 'S3 URI',
            'description': 'The S3 URI of public file object.',
            'comment': 'Do not submit. Value is calculated from file metadata.',
            'type': 'string',
            'notSubmittable': True,
        },
        define=True,
    )
    def s3_uri(self):
        try:
            external = self._get_external_sheet()
        except HTTPNotFound:
            return None
        return 's3://{bucket}/{key}'.format(**external)

    @calculated_property(
        condition=show_upload_credentials,
        schema={
            'title': 'Upload Credentials',
            'description': 'The upload credentials for S3 to submit the file content.',
            'comment': 'Do not submit. This is issued by the server.',
            'type': 'object',
        }
    )
    def upload_credentials(self):
        external = self.propsheets.get('external', None)
        if external is not None:
            return external.get('upload_credentials', None)

    @classmethod
    def create(cls, registry, uuid, properties, sheets=None):
        if properties.get('upload_status') == 'pending':
            sheets = {} if sheets is None else sheets.copy()
            if properties.get('controlled_access') is True:
                bucket = registry.settings['restricted_file_upload_bucket']
                sts_client = get_restricted_sts_client(
                    localstack_endpoint_url=os.environ.get(
                        'LOCALSTACK_ENDPOINT_URL'
                    )
                )
            else:
                bucket = registry.settings['file_upload_bucket']
                sts_client = get_sts_client(
                    localstack_endpoint_url=os.environ.get(
                        'LOCALSTACK_ENDPOINT_URL'
                    )
                )
            file_extension = FILE_FORMAT_TO_FILE_EXTENSION[properties['file_format']]
            date = properties['creation_timestamp'].split('T')[0].replace('-', '/')
            accession = properties.get('accession')
            key = f'{date}/{uuid}/{accession}{file_extension}'
            name = f'up{time.time():.6f}-{accession}'[:32]  # max 32 chars
            upload_credentials = UploadCredentials(
                bucket=bucket,
                key=key,
                name=name,
                sts_client=sts_client,
            )
            sheets['external'] = upload_credentials.external_creds()
        return super(File, cls).create(registry, uuid, properties, sheets)

    def _get_external_sheet(self):
        external = self.propsheets.get(
            'external',
            {}
        )
        if external.get('service') == 's3':
            return external
        else:
            raise HTTPNotFound()

    def _set_external_sheet(self, new_external):
        # This just updates external sheet, doesn't overwrite.
        external = self._get_external_sheet()
        external = external.copy()
        external.update(
            new_external
        )
        properties = self.upgrade_properties()
        self.update(
            properties,
            {
                'external': external
            }
        )


@collection(
    name='sequence-files',
    unique_key='accession',
    properties={
        'title': 'Sequence Files',
        'description': 'Listing of sequence data files',
    }
)
class SequenceFile(File):
    item_type = 'sequence_file'
    schema = load_schema('igvfd:schemas/sequence_file.json')
    embedded_with_frame = File.embedded_with_frame
    rev = File.rev | {
        'seqspecs': ('ConfigurationFile', 'seqspec_of')
    }
    set_status_up = File.set_status_up + [
        'sequencing_platform'
    ]
    set_status_down = File.set_status_down + []

    def unique_keys(self, properties):
        keys = super(File, self).unique_keys(properties)
        if properties.get('status') not in ['deleted', 'replaced', 'revoked']:
            if 'md5sum' in properties:
                value = 'md5:{md5sum}'.format(**properties)
                keys.setdefault('alias', []).append(value)
        if properties.get('status') not in ['deleted', 'replaced']:
            value_list = []
            illumina_read_type = properties.get('illumina_read_type', '')
            sequencing_run = str(properties.get('sequencing_run', ''))
            flowcell_id = properties.get('flowcell_id', '')
            lane = str(properties.get('lane', ''))
            file_set = properties.get('file_set', '')
            index = properties.get('index', '')
            value_list += file_set, illumina_read_type, sequencing_run, flowcell_id, lane, index
            if properties.get('status') == 'released' and properties.get('derived_from', None):
                value_list += [properties.get('status')]
            value_list = [item for item in value_list if item != '']
            value = ':'.join(value_list)
            if not properties.get('derived_from', None) or \
                    (properties.get('status') == 'released' and properties.get('derived_from', None)):
                keys.setdefault('sequencing_run', []).append(value)
        return keys

    @calculated_property(schema={
        'title': 'Seqspecs',
        'description': 'Link(s) to the associated seqspec YAML configuration file(s).',
        'type': 'array',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Seqspecs',
            'type': ['string', 'object'],
            'linkFrom': 'ConfigurationFile.seqspec_of',
        },
        'notSubmittable': True
    })
    def seqspecs(self, request, seqspecs):
        return paths_filtered_by_status(request, seqspecs)


@collection(
    name='reference-files',
    unique_key='accession',
    properties={
        'title': 'Reference Files',
        'description': 'Listing of reference data files',
    }
)
class ReferenceFile(File):
    item_type = 'reference_file'
    schema = load_schema('igvfd:schemas/reference_file.json')
    embedded_with_frame = File.embedded_with_frame
    set_status_up = File.set_status_up + []
    set_status_down = File.set_status_down + []

    def unique_keys(self, properties):
        keys = super(File, self).unique_keys(properties)
        if properties.get('status') not in ['deleted', 'replaced', 'revoked']:
            if 'md5sum' in properties:
                value = 'md5:{md5sum}'.format(**properties)
                keys.setdefault('alias', []).append(value)
            if 'external_id' in properties:
                value = 'external:{external_id}'.format(**properties)
                keys.setdefault('alias', []).append(value)
        return keys


@collection(
    name='alignment-files',
    unique_key='accession',
    properties={
        'title': 'Alignment Files',
        'description': 'Listing of alignment files',
    }
)
class AlignmentFile(File):
    item_type = 'alignment_file'
    schema = load_schema('igvfd:schemas/alignment_file.json')
    embedded_with_frame = File.embedded_with_frame
    set_status_up = File.set_status_up + []
    set_status_down = File.set_status_down + []

    def unique_keys(self, properties):
        keys = super(File, self).unique_keys(properties)
        if properties.get('status') not in ['deleted', 'replaced', 'revoked']:
            if 'md5sum' in properties:
                value = 'md5:{md5sum}'.format(**properties)
                keys.setdefault('alias', []).append(value)
        return keys

    @calculated_property(
        schema={
            'title': 'Content Summary',
            'type': 'string',
            'description': 'A summary of the data in the alignment file.',
            'notSubmittable': True
        }
    )
    def content_summary(self, request, content_type, redacted, filtered):
        redacted_phrase = ''
        if redacted:
            redacted_phrase = 'redacted'

        filtered_phrase = 'unfiltered'
        if filtered:
            filtered_phrase = 'filtered'

        phrases = [
            filtered_phrase,
            redacted_phrase,
            content_type
        ]
        non_empty_phrases = [x for x in phrases if x != '']
        return ' '.join(non_empty_phrases)


@collection(
    name='matrix-files',
    unique_key='accession',
    properties={
        'title': 'Matrix Files',
        'description': 'Listing of matrix files',
    }
)
class MatrixFile(File):
    item_type = 'matrix_file'
    schema = load_schema('igvfd:schemas/matrix_file.json')
    embedded_with_frame = File.embedded_with_frame
    set_status_up = File.set_status_up + []
    set_status_down = File.set_status_down + []

    def unique_keys(self, properties):
        keys = super(File, self).unique_keys(properties)
        if properties.get('status') not in ['deleted', 'replaced', 'revoked']:
            if 'md5sum' in properties:
                value = 'md5:{md5sum}'.format(**properties)
                keys.setdefault('alias', []).append(value)
        return keys

    @calculated_property(
        schema={
            'title': 'Content Summary',
            'type': 'string',
            'description': 'A summary of the data in the matrix file.',
            'notSubmittable': True
        }
    )
    def content_summary(self, request, dimension1, dimension2, content_type):
        return f'{dimension1} by {dimension2} {content_type}'


@collection(
    name='signal-files',
    unique_key='accession',
    properties={
        'title': 'Signal Files',
        'description': 'Listing of signal files',
    }
)
class SignalFile(File):
    item_type = 'signal_file'
    schema = load_schema('igvfd:schemas/signal_file.json')
    embedded_with_frame = File.embedded_with_frame
    set_status_up = File.set_status_up + []
    set_status_down = File.set_status_down + []

    def unique_keys(self, properties):
        keys = super(File, self).unique_keys(properties)
        if properties.get('status') not in ['deleted', 'replaced', 'revoked']:
            if 'md5sum' in properties:
                value = 'md5:{md5sum}'.format(**properties)
                keys.setdefault('alias', []).append(value)
        return keys

    @calculated_property(
        schema={
            'title': 'Content Summary',
            'type': 'string',
            'description': 'A summary of the data in the signal file.',
            'notSubmittable': True
        }
    )
    def content_summary(self, request, content_type, strand_specificity, filtered, normalized):
        filtered_phrase = ''
        if filtered:
            filtered_phrase = 'filtered'

        normalized_phrase = ''
        if normalized:
            normalized_phrase = 'normalized'

        strand_phrase = strand_specificity
        if strand_phrase != 'unstranded':
            strand_phrase += ' strand'

        phrases = [
            filtered_phrase,
            normalized_phrase,
            strand_phrase,
            content_type
        ]
        non_empty_phrases = [x for x in phrases if x != '']
        return ' '.join(non_empty_phrases)


@collection(
    name='configuration-files',
    unique_key='accession',
    properties={
        'title': 'Configuration Files',
        'description': 'Listing of configuration files',
    }
)
class ConfigurationFile(File):
    item_type = 'configuration_file'
    schema = load_schema('igvfd:schemas/configuration_file.json')
    embedded_with_frame = File.embedded_with_frame
    set_status_up = File.set_status_up + []
    set_status_down = File.set_status_down + []

    def unique_keys(self, properties):
        keys = super(File, self).unique_keys(properties)
        if properties.get('status') not in ['deleted', 'replaced', 'revoked']:
            if 'md5sum' in properties:
                value = 'md5:{md5sum}'.format(**properties)
                keys.setdefault('alias', []).append(value)
        return keys


@collection(
    name='tabular-files',
    unique_key='accession',
    properties={
        'title': 'Tabular Files',
        'description': 'Listing of tabular files',
    }
)
class TabularFile(File):
    item_type = 'tabular_file'
    schema = load_schema('igvfd:schemas/tabular_file.json')
    embedded_with_frame = File.embedded_with_frame
    set_status_up = File.set_status_up + []
    set_status_down = File.set_status_down + []

    def unique_keys(self, properties):
        keys = super(File, self).unique_keys(properties)
        if properties.get('status') not in ['deleted', 'replaced', 'revoked']:
            if 'md5sum' in properties:
                value = 'md5:{md5sum}'.format(**properties)
                keys.setdefault('alias', []).append(value)
        return keys


@collection(
    name='genome-browser-annotation-files',
    unique_key='accession',
    properties={
        'title': 'Genome Browser Annotation Files',
        'description': 'Listing of genome browser annotation files',
    }
)
class GenomeBrowserAnnotationFile(File):
    item_type = 'genome_browser_annotation_file'
    schema = load_schema('igvfd:schemas/genome_browser_annotation_file.json')
    embedded_with_frame = File.embedded_with_frame
    set_status_up = File.set_status_up + []
    set_status_down = File.set_status_down + []

    def unique_keys(self, properties):
        keys = super(File, self).unique_keys(properties)
        if properties.get('status') not in ['deleted', 'replaced', 'revoked']:
            if 'md5sum' in properties:
                value = 'md5:{md5sum}'.format(**properties)
                keys.setdefault('alias', []).append(value)
        return keys


@collection(
    name='image-files',
    unique_key='accession',
    properties={
        'title': 'Image Files',
        'description': 'Listing of image files',
    }
)
class ImageFile(File):
    item_type = 'image_file'
    schema = load_schema('igvfd:schemas/image_file.json')
    embedded_with_frame = File.embedded_with_frame
    set_status_up = File.set_status_up + []
    set_status_down = File.set_status_down + []

    def unique_keys(self, properties):
        keys = super(File, self).unique_keys(properties)
        if properties.get('status') not in ['deleted', 'replaced', 'revoked']:
            if 'md5sum' in properties:
                value = 'md5:{md5sum}'.format(**properties)
                keys.setdefault('alias', []).append(value)
        return keys


@collection(
    name='model-files',
    unique_key='accession',
    properties={
        'title': 'Model Files',
        'description': 'Listing of model files',
    }
)
class ModelFile(File):
    item_type = 'model_file'
    schema = load_schema('igvfd:schemas/model_file.json')
    embedded_with_frame = File.embedded_with_frame
    set_status_up = File.set_status_up + []
    set_status_down = File.set_status_down + []

    def unique_keys(self, properties):
        keys = super(File, self).unique_keys(properties)
        if properties.get('status') not in ['deleted', 'replaced', 'revoked']:
            if 'md5sum' in properties:
                value = 'md5:{md5sum}'.format(**properties)
                keys.setdefault('alias', []).append(value)
        return keys


@view_config(
    name='upload',
    context=File,
    request_method='GET',
    permission='edit'
)
def get_upload(context, request):
    properties = context.upgrade_properties()
    external = context.propsheets.get('external', {})
    upload_credentials = external.get('upload_credentials')
    # Show s3 location info for files originally submitted to EDW.
    if upload_credentials is None and external.get('service') == 's3':
        upload_credentials = {
            'upload_url': 's3://{bucket}/{key}'.format(**external),
        }
    return {
        '@graph': [
            {
                '@id': request.resource_path(context),
                'upload_credentials': upload_credentials,
            }
        ],
    }


def validate_bucket_location(request, properties, bucket):
    if properties.get('controlled_access') is True:
        if bucket != request.registry.settings['restricted_file_upload_bucket']:
            raise HTTPForbidden(
                f'File is controlled_access=True but was created using bucket {bucket}'
            )
    else:
        if bucket != request.registry.settings['file_upload_bucket']:
            raise HTTPForbidden(
                f'File is controlled_access=False but was created using bucket {bucket}'
            )


@view_config(
    name='upload',
    context=File,
    request_method='POST',
    permission='edit',
    validators=[
        schema_validator(
            {
                'type': 'object'
            }
        )
    ]
)
def post_upload(context, request):
    properties = context.upgrade_properties()
    if properties['upload_status'] == 'validated':
        raise HTTPForbidden(
            'Unable to issue new credentials when uploading_status is validated'
        )
    external = context.propsheets.get(
        'external',
        {}
    )
    if external.get('service') != 's3':
        raise HTTPNotFound(
            detail=f'External service {external.get("service")} not expected'
        )
    bucket = external['bucket']
    key = external['key']
    accession = properties['accession']
    name = f'up{time.time():.6f}-{accession}'[:32]  # max 32 chars
    validate_bucket_location(request, properties, bucket)
    if properties.get('controlled_access') is True:
        sts_client = get_restricted_sts_client(
            localstack_endpoint_url=os.environ.get(
                'LOCALSTACK_ENDPOINT_URL'
            )
        )
    else:
        sts_client = get_sts_client(
            localstack_endpoint_url=os.environ.get(
                'LOCALSTACK_ENDPOINT_URL'
            )
        )
    upload_credentials = UploadCredentials(
        bucket=bucket,
        key=key,
        name=name,
        sts_client=sts_client,
    )
    external_credentials = upload_credentials.external_creds()
    new_properties = None
    if properties['upload_status'] != 'pending':
        new_properties = properties.copy()
        new_properties['upload_status'] = 'pending'
        new_properties.pop('validation_error_detail', None)
    request.registry.notify(
        BeforeModified(
            context,
            request
        )
    )
    context.update(
        new_properties,
        {
            'external': external_credentials
        }
    )
    request.registry.notify(
        AfterModified(
            context,
            request
        )
    )
    rendered = request.embed(
        f'/{str(context.uuid)}/@@object',
        as_user=True
    )
    result = {
        'status': 'success',
        '@type': ['result'],
        '@graph': [rendered],
    }
    return result


@view_config(
    name='download',
    context=File,
    request_method='GET',
    permission='view',
    subpath_segments=[0, 1]
)
def download(context, request):
    properties = context.upgrade_properties()
    if properties.get('anvil_url') is not None:
        raise HTTPForbidden(
            'Downloading Anvil file not allowed.'
        )
    file_extension = FILE_FORMAT_TO_FILE_EXTENSION[properties['file_format']]
    accession = properties['accession']
    filename = f'{accession}{file_extension}'
    if request.subpath:
        _filename, = request.subpath
        if filename != _filename:
            raise HTTPNotFound(
                _filename
            )
    external = context.propsheets.get('external', {})
    if external.get('service') != 's3':
        raise HTTPNotFound(
            detail=f'External service {external.get("service")} not expected'
        )
    bucket = external['bucket']
    key = external['key']
    validate_bucket_location(request, properties, bucket)
    s3_client = get_s3_client(
        localstack_endpoint_url=os.environ.get(
            'LOCALSTACK_ENDPOINT_URL'
        )
    )
    location = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket,
            'Key': key,
            'ResponseContentDisposition': 'attachment; filename=' + filename
        },
        ExpiresIn=36*60*60,
    )
    if asbool(request.params.get('soft')):
        expires = int(parse_qs(urlparse(location).query)['Expires'][0])
        return {
            '@type': ['SoftRedirect'],
            'location': location,
            'expires': datetime.datetime.fromtimestamp(expires, pytz.utc).isoformat(),
        }
    proxy = asbool(request.params.get('proxy'))
    accel_redirect_header = request.registry.settings.get('accel_redirect_header')
    if proxy and accel_redirect_header:
        return InternalRedirect(headers={accel_redirect_header: '/_proxy/' + str(location)})
    raise HTTPTemporaryRedirect(location=location)
