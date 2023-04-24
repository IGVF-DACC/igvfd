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

from igvfd.types.base import Item

from igvfd.upload_credentials import get_s3_client
from igvfd.upload_credentials import get_sts_client
from igvfd.upload_credentials import UploadCredentials

from igvfd.checkfiles_credentials import get_checkfiles_mount_credentials


FILE_FORMAT_TO_FILE_EXTENSION = {
    '2bit': '.2bit',
    'CEL': '.cel.gz',
    'bam': '.bam',
    'bed': '.bed.gz',
    'bedpe': '.bedpe.gz',
    'chain': '.chain',
    'bigBed': '.bigBed',
    'bigInteract': '.bigInteract',
    'bigWig': '.bigWig',
    'btr': '.btr',
    'csfasta': '.csfasta.gz',
    'csqual': '.csqual.gz',
    'cndb': '.cndb',
    'database': '.db',
    'fasta': '.fasta.gz',
    'fastq': '.fastq.gz',
    'gff': '.gff.gz',
    'gtf': '.gtf.gz',
    'idx': '.idx',
    'hic': '.hic',
    'h5ad': '.h5ad',
    'hdf5': '.h5',
    'idat': '.idat',
    'PWM': '.pwm',
    'rcc': '.rcc',
    'sra': '.sra',
    'tagAlign': '.tagAlign.gz',
    'tar': '.tar.gz',
    'tsv': '.tsv',
    'csv': '.csv',
    'vcf': '.vcf.gz',
    'wig': '.wig.gz',
    'sam': '.sam.gz',
    'txt': '.txt.gz',
    'pairs': '.pairs.gz',
    'starch': '.starch',
    'nucle3d': '.nucle3d',
}


def show_upload_credentials(request=None, context=None, upload_status=None):
    if request is None or upload_status == 'validated':
        return False
    return request.has_permission('edit', context)


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

    @calculated_property(
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
            bucket = registry.settings['file_upload_bucket']
            file_extension = FILE_FORMAT_TO_FILE_EXTENSION[properties['file_format']]
            date = properties['creation_timestamp'].split('T')[0].replace('-', '/')
            accession = properties.get('accession')
            key = f'{date}/{uuid}/{accession}{file_extension}'
            name = f'up{time.time():.6f}-{accession}'[:32]  # max 32 chars
            profile_name = registry.settings.get('file_upload_profile_name')
            upload_credentials = UploadCredentials(
                bucket=bucket,
                key=key,
                name=name,
                sts_client=get_sts_client(
                    localstack_endpoint_url=os.environ.get(
                        'LOCALSTACK_ENDPOINT_URL'
                    )
                ),
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
    name='sequence-data',
    unique_key='accession',
    properties={
        'title': 'Sequence Data',
        'description': 'Listing of sequence data files',
    }
)
class SequenceData(File):
    item_type = 'sequence_data'
    schema = load_schema('igvfd:schemas/sequence_data.json')
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
    ]

    def unique_keys(self, properties):
        keys = super(File, self).unique_keys(properties)
        if properties.get('status') != 'replaced':
            if 'md5sum' in properties:
                value = 'md5:{md5sum}'.format(**properties)
                keys.setdefault('alias', []).append(value)
        if properties.get('status') not in ['deleted', 'replaced']:
            if 'illumina_read_type' in properties:
                value = f'sequencing_run:{properties["file_set"]}:{properties["sequencing_run"]}:{properties["illumina_read_type"]}'
            else:
                value = f'sequencing_run:{properties["file_set"]}:{properties["sequencing_run"]}'
            keys.setdefault('sequencing_run', []).append(value)
        return keys


@collection(
    name='reference-data',
    unique_key='accession',
    properties={
        'title': 'Reference Data',
        'description': 'Listing of reference data files',
    }
)
class ReferenceData(File):
    item_type = 'reference_data'
    schema = load_schema('igvfd:schemas/reference_data.json')
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
    ]

    def unique_keys(self, properties):
        keys = super(File, self).unique_keys(properties)
        if properties.get('status') != 'replaced':
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
    if external.get('service') == 's3':
        bucket = external['bucket']
        key = external['key']
    else:
        raise HTTPNotFound(
            detail=f'External service {external.get("service")} not expected'
        )
    accession = properties['accession']
    name = f'up{time.time():.6f}-{accession}'[:32]  # max 32 chars
    file_upload_bucket = request.registry.settings['file_upload_bucket']
    profile_name = request.registry.settings.get('file_upload_profile_name')
    upload_credentials = UploadCredentials(
        bucket=bucket,
        key=key,
        name=name,
        sts_client=get_sts_client(
            localstack_endpoint_url=os.environ.get(
                'LOCALSTACK_ENDPOINT_URL'
            )
        ),
    )
    external_credentials = upload_credentials.external_creds()
    new_properties = None
    if properties['upload_status'] != 'pending':
        new_properties = properties.copy()
        new_properties['upload_status'] = 'pending'
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
    if external.get('service') == 's3':
        s3_client = get_s3_client(
            localstack_endpoint_url=os.environ.get(
                'LOCALSTACK_ENDPOINT_URL'
            )
        )
        location = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': external['bucket'],
                'Key': external['key'],
                'ResponseContentDisposition': 'attachment; filename=' + filename
            },
            ExpiresIn=36*60*60,
        )
    else:
        raise HTTPNotFound(
            detail=f'External service {external.get("service")} not expected'
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


@view_config(
    name='readcredentials',
    context=File,
    request_method='GET',
    permission='view'
)
def get_read_token(context, request):
    external = context.propsheets.get('external', {})
    bucket = external.get('bucket')
    credentials = get_checkfiles_mount_credentials()
    return {
        'bucket': bucket,
        'credentials': credentials,
    }
