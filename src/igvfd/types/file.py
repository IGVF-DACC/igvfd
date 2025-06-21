import datetime
import os
import pytz
import time

from pyramid.authorization import (
    Allow,
    Deny,
    Everyone,
)

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

from igvfd.audit.file_set import (
    SINGLE_CELL_ASSAY_TERMS
)

from igvfd.upload_credentials import get_s3_client
from igvfd.upload_credentials import get_sts_client
from igvfd.upload_credentials import get_restricted_sts_client
from igvfd.upload_credentials import UploadCredentials


# Consortium members (viewing group members) can download controlled_access files.
ALLOW_DOWNLOAD_CONTROLLED_ACCESS_FILE = [
    (Allow, 'role.viewing_group_member', 'download_controlled_access_file'),
    (Allow, 'group.admin', 'download_controlled_access_file'),
    (Allow, 'group.read-only-admin', 'download_controlled_access_file'),
    (Deny, Everyone, 'download_controlled_access_file'),
]


FILE_FORMAT_TO_FILE_EXTENSION = {
    'bai': '.bai',
    'bam': '.bam',
    'bed': '.bed.gz',
    'bedpe': '.bedpe.gz',
    'bigBed': '.bigBed',
    'bigInteract': '.bigInteract',
    'bigWig': '.bigWig',
    'cool': '.cool',
    'mcool': '.mcool',
    'crai': '.crai',
    'cram': '.cram',
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
    'mtx': '.mtx.gz',
    'npz': 'npz',
    'obo': '.obo.gz',
    'owl': '.owl.gz',
    'pairs': '.pairs.gz',
    'pkl': 'pkl',
    'pod5': '.pod5',
    'png': '.png',
    'pt': '.pt',
    'PWM': '.pwm',
    'Robj': '.Robj',
    'sam': '.sam.gz',
    'sra': '.sra',
    'tagAlign': '.tagAlign.gz',
    'tar': '.tar.gz',
    'tbi': '.tbi',
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


def show_href():
    return True


def show_s3uri():
    return True


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
        Path('file_set.samples.disease_terms', include=[
             '@id', 'accession', 'status', 'summary', 'samples', 'disease_terms', 'sample_terms', 'assay_term', 'term_name', 'classifications', 'file_set_type', 'taxa', 'targeted_sample_term', 'modifications', 'treatments', '@type', 'data_use_limitation_summaries', 'controlled_access']),
        Path('file_set.samples.sample_terms', include=[
             '@id', 'term_name', 'status']),
        Path('file_set.samples.targeted_sample_term', include=[
             '@id', 'term_name', 'status']),
        Path('file_set.samples.modifications', include=[
             '@id', 'modality', 'summary', 'status']),
        Path('file_set.samples.treatments', include=[
             '@id', 'purpose', 'summary', 'treatment_term_name', 'status']),
        Path('integrated_in.associated_phenotypes', include=[
             '@id', 'summary', 'status', 'file_set_type', 'associated_phenotypes', 'term_name', 'small_scale_gene_list', 'applied_to_samples']),
        Path('integrated_in.small_scale_gene_list', include=['@id', 'symbol', 'status']),
        Path('integrated_in.applied_to_samples.sample_terms', include=['@id', 'summary', 'sample_terms', 'term_name']),
        Path('workflow', include=['@id', 'uniform_pipeline', 'name']),
        Path('file_set.assay_term', include=['@id', 'term_name']),
        Path('file_format_specifications', include=['@id', 'description', 'standardized_file_format'])
    ]
    rev = {
        'integrated_in': ('ConstructLibrarySet', 'integrated_content_files'),
        'gene_list_for': ('FileSet', 'large_scale_gene_list'),
        'loci_list_for': ('FileSet', 'large_scale_loci_list'),
        'input_file_for': ('File', 'derived_from'),
        'quality_metrics': ('QualityMetric', 'quality_metric_of')
    }

    set_status_up = [
        'analysis_step_version',
        'file_format_specifications'
    ]
    set_status_down = []

    def __acl__(self):
        return ALLOW_DOWNLOAD_CONTROLLED_ACCESS_FILE + super().__acl__()

    @calculated_property(schema={
        'title': 'Integrated In',
        'description': 'Construct library set(s) that this file was used for in insert design.',
        'type': 'array',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Integrated In',
            'type': 'string',
            'linkFrom': 'ConstructLibrarySet.integrated_content_files',
        },
        'notSubmittable': True
    })
    def integrated_in(self, request, integrated_in):
        return paths_filtered_by_status(request, integrated_in)

    @calculated_property(schema={
        'title': 'Input File For',
        'description': 'The files which are derived from this file.',
        'type': 'array',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Input File For',
            'type': 'string',
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
            'type': 'string',
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
            'type': 'string',
            'linkFrom': 'FileSet.large_scale_loci_list',
        },
        'notSubmittable': True
    })
    def loci_list_for(self, request, loci_list_for):
        return paths_filtered_by_status(request, loci_list_for)

    @calculated_property(schema={
        'title': 'Quality Metrics',
        'description': 'The quality metrics that are associated with this file.',
        'type': 'array',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Quality Metric',
            'type': 'string',
            'linkFrom': 'QualityMetric.quality_metric_of',
        },
        'notSubmittable': True
    })
    def quality_metrics(self, request, quality_metrics):
        return paths_filtered_by_status(request, quality_metrics)

    @calculated_property(
        schema={
            'title': 'Assay Titles',
            'description': 'Title(s) of assay from the file set this file belongs to.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Assay Title',
                'description': 'Title of assay from the file set this file belongs to.',
                'type': 'string'
            },
            'notSubmittable': True,
        }
    )
    def assay_titles(self, request, file_set):
        assay_titles = set()
        file_set_object = request.embed(file_set, '@@object')
        if 'MeasurementSet' in file_set_object.get('@type'):
            preferred_assay_title = file_set_object.get('preferred_assay_title', '')
            if preferred_assay_title:
                assay_titles.add(preferred_assay_title)
        elif 'AnalysisSet' in file_set_object.get('@type'):
            analysis_assay_titles = set(file_set_object.get('assay_titles', []))
            if analysis_assay_titles:
                assay_titles = assay_titles | analysis_assay_titles
        elif 'AuxiliarySet' in file_set_object.get('@type'):
            for measurement_set in file_set_object.get('measurement_sets'):
                measurement_set_object = request.embed(measurement_set, '@@object')
                measurement_set_object_pat = measurement_set_object.get('preferred_assay_title')
                if measurement_set_object_pat:
                    assay_titles.add(measurement_set_object_pat)
        return sorted(list(assay_titles))

    @calculated_property(
        condition='analysis_step_version',
        schema={
            'title': 'Workflow',
            'description': 'The workflow used to produce this file.',
            'type': 'string',
            'linkTo': 'Workflow',
            'notSubmittable': True,
        }
    )
    def workflow(self, request, analysis_step_version):
        if analysis_step_version:
            analysis_step_version_object = request.embed(analysis_step_version, '@@object')
            analysis_step = analysis_step_version_object.get('analysis_step', '')
            if analysis_step:
                analysis_step_object = request.embed(analysis_step, '@@object')
                workflow = analysis_step_object.get('workflow', '')
                if workflow:
                    return workflow

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
    embedded_with_frame = File.embedded_with_frame + [
        Path('sequencing_platform', include=['@id', 'term_name', 'status']),
    ]
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
            'type': 'string',
            'linkFrom': 'ConfigurationFile.seqspec_of',
        },
        'notSubmittable': True
    })
    def seqspecs(self, request, seqspecs):
        return paths_filtered_by_status(request, seqspecs)

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'description': 'A summary of the sequence file.',
            'notSubmittable': True,
        }
    )
    def summary(self, content_type, sequencing_run, illumina_read_type=None):
        prefix = content_type
        if illumina_read_type:
            prefix = f'{illumina_read_type} {content_type}'
        return f'{prefix} from sequencing run {sequencing_run}'


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

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'description': 'A summary of the reference file.',
            'notSubmittable': True,
        }
    )
    def summary(self, request, content_type, file_set, assembly=None, transcriptome_annotation=None):
        file_set_object = request.embed(file_set, '@@object_with_select_calculated_properties?field=@type')
        predicted = None
        if 'PredictionSet' in file_set_object['@type']:
            predicted = 'predictive'
        formatted_assembly = assembly
        if assembly and assembly == 'custom':
            formatted_assembly = f'{assembly} assembly'
        return ' '.join(
            [x for x in [formatted_assembly, transcriptome_annotation, predicted, content_type]
             if x is not None]
        )


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
        define=True,
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

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'description': 'A summary of the alignment file.',
            'notSubmittable': True,
        }
    )
    def summary(self, request, content_summary, file_set, assembly=None, transcriptome_annotation=None):
        file_set_object = request.embed(file_set, '@@object_with_select_calculated_properties?field=@type')
        predicted = None
        if 'PredictionSet' in file_set_object['@type']:
            predicted = 'predictive'
        formatted_assembly = assembly
        if assembly and assembly == 'custom':
            formatted_assembly = f'{assembly} assembly'
        return ' '.join(
            [x for x in [formatted_assembly, transcriptome_annotation, predicted, content_summary]
             if x is not None]
        )


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
        define=True,
        schema={
            'title': 'Content Summary',
            'type': 'string',
            'description': 'A summary of the data in the matrix file.',
            'notSubmittable': True
        }
    )
    def content_summary(self, principal_dimension, secondary_dimensions, content_type):
        secondary_dimensions_str = f'{" by ".join(secondary_dimensions)}'
        return f'{principal_dimension} by {secondary_dimensions_str} in {content_type}'

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'description': 'A summary of the matrix file.',
            'notSubmittable': True,
        }
    )
    def summary(self, request, content_summary, file_set, filtered=None, analysis_step_version=None):
        file_set_object = request.embed(file_set, '@@object_with_select_calculated_properties?field=@type')
        predicted = None
        if 'PredictionSet' in file_set_object['@type']:
            predicted = 'predictive'
        software_version_phrase = None
        if analysis_step_version and predicted is not None:
            software_versions = set()
            asv_object = request.embed(analysis_step_version, '@@object?skip_calculated=true')
            for software_version in asv_object['software_versions']:
                software_version_object = request.embed(
                    software_version, '@@object_with_select_calculated_properties?field=summary')
                software_versions.add(software_version_object['summary'])
            software_version_phrase = f'({", ".join(sorted(software_versions))})'
        filtered_phrase = None
        if filtered is True:
            filtered_phrase = 'filtered'
        elif filtered is False:
            filtered_phrase = 'unfiltered'
        return ' '.join(
            [x for x in [predicted, filtered_phrase, content_summary, software_version_phrase] if x is not None]
        )

    @calculated_property(
        schema={
            'title': 'Transcriptome Annotation',
            'type': 'string',
            'description': 'The annotation and version of the reference resource.',
            'notSubmittable': True
        }
    )
    def transcriptome_annotation(self, request, reference_files):
        transcriptome_annotation_set = set()
        transcriptome_annotation = ''
        for ref_file in reference_files:
            ref_file_object = request.embed(ref_file, '@@object?skip_calculated=true')
            if ref_file_object['content_type'] == 'transcriptome reference':
                transcriptome_annotation_set.add(ref_file_object.get('transcriptome_annotation', ''))
        if len(transcriptome_annotation_set) > 1:
            transcriptome_annotation = 'mixed'
        elif len(transcriptome_annotation_set) == 1:
            transcriptome_annotation = list(transcriptome_annotation_set)[0]
        return transcriptome_annotation

    @calculated_property(
        schema={
            'title': 'Genome Assembly',
            'type': 'string',
            'description': 'The assembly associated with the matrix file.',
            'notSubmittable': True
        }
    )
    def assembly(self, request, reference_files):
        assembly_set = set()
        assembly = ''
        for ref_file in reference_files:
            ref_file_object = request.embed(ref_file, '@@object?skip_calculated=true')
            if ref_file_object['content_type'] == 'genome reference':
                assembly_set.add(ref_file_object.get('assembly', ''))
        if len(assembly_set) > 1:
            assembly = 'mixed'
        elif len(assembly_set) == 1:
            assembly = list(assembly_set)[0]
        return assembly


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
    embedded_with_frame = File.embedded_with_frame + [
        Path('cell_type_annotation', include=['@id', 'term_name', 'status'])
    ]
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
        define=True,
        schema={
            'title': 'Content Summary',
            'type': 'string',
            'description': 'A summary of the data in the signal file.',
            'notSubmittable': True
        }
    )
    def content_summary(self, content_type, strand_specificity, filtered=None, normalized=None):
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

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'description': 'A summary of the signal file.',
            'notSubmittable': True,
        }
    )
    def summary(self, request, content_summary, file_set, assembly=None, transcriptome_annotation=None, analysis_step_version=None):
        file_set_object = request.embed(file_set, '@@object_with_select_calculated_properties?field=@type')
        predicted = None
        if 'PredictionSet' in file_set_object['@type']:
            predicted = 'predictive'
        software_version_phrase = None
        if analysis_step_version and predicted is not None:
            software_versions = set()
            asv_object = request.embed(analysis_step_version, '@@object?skip_calculated=true')
            for software_version in asv_object['software_versions']:
                software_version_object = request.embed(
                    software_version, '@@object_with_select_calculated_properties?field=summary')
                software_versions.add(software_version_object['summary'])
            software_version_phrase = f'({", ".join(sorted(software_versions))})'
        formatted_assembly = assembly
        if assembly and assembly == 'custom':
            formatted_assembly = f'{assembly} assembly'
        return ' '.join(
            [x for x in [formatted_assembly, transcriptome_annotation, predicted, content_summary, software_version_phrase]
             if x is not None]
        )


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

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'description': 'A summary of the configuration file.',
            'notSubmittable': True,
        }
    )
    def summary(self, request, file_set, content_type, seqspec_of=None, analysis_step_version=None):
        seqspec_of_formatted = None
        if seqspec_of:
            file_accessions = [x.split('/')[-2] for x in seqspec_of]
            seqspec_of_formatted = f"of {', '.join(file_accessions)}"
        file_set_object = request.embed(file_set, '@@object_with_select_calculated_properties?field=@type')
        predicted = None
        if 'PredictionSet' in file_set_object['@type']:
            predicted = 'predictive'
        software_version_phrase = None
        if analysis_step_version and predicted is not None:
            software_versions = set()
            asv_object = request.embed(analysis_step_version, '@@object?skip_calculated=true')
            for software_version in asv_object['software_versions']:
                software_version_object = request.embed(
                    software_version, '@@object_with_select_calculated_properties?field=summary')
                software_versions.add(software_version_object['summary'])
            software_version_phrase = f'({", ".join(sorted(software_versions))})'
        return ' '.join(
            [x for x in [predicted, content_type, seqspec_of_formatted, software_version_phrase]
             if x is not None]
        )

    @calculated_property(
        schema={
            'title': 'Validate Onlist Files',
            'type': 'boolean',
            'description': 'Whether checkfiles will validate the onlist files.',
            'notSubmittable': True
        }
    )
    def validate_onlist_files(self, request, content_type, seqspec_of=None):
        # Validate onlist files if the file is not linked to a single cell assay measurement set
        # If not seqspec, return False
        if content_type != 'seqspec':
            return False
        # Get the file set object
        if not seqspec_of:
            return False
        # Get all file sets linked to the seqspec files
        linked_file_sets = sorted(
            set([request.embed(seqfile, '@@object?skip_calculated_properties=true').get('file_set') for seqfile in seqspec_of]))
        # If none is a measurement set, return False
        if all([not file_set.startswith('/measurement-sets/') for file_set in linked_file_sets]):
            return False
        # Get assay terms for all the measurement sets
        assay_terms = sorted(set([request.embed(
            file_set, '@@object?skip_calculated_properties=true').get('assay_term', '') for file_set in linked_file_sets]))
        # Check if any of the assay terms are single cell assay terms
        return any([assay_term in SINGLE_CELL_ASSAY_TERMS for assay_term in assay_terms])


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
    embedded_with_frame = File.embedded_with_frame + [
        Path('cell_type_annotation', include=['@id', 'term_name', 'status'])
    ]
    rev = File.rev | {
        'barcode_map_for': ('MultiplexedSample', 'barcode_map'),
        'primer_design_for': ('MeasurementSet', 'primer_designs')
    }

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
            'title': 'Summary',
            'type': 'string',
            'description': 'A summary of the tabular file.',
            'notSubmittable': True,
        }
    )
    def summary(self, request, content_type, file_set, assembly=None, transcriptome_annotation=None, filtered=None, analysis_step_version=None):
        file_set_object = request.embed(file_set, '@@object_with_select_calculated_properties?field=@type')
        predicted = None
        if 'PredictionSet' in file_set_object['@type']:
            predicted = 'predictive'
        formatted_assembly = assembly
        if assembly and assembly == 'custom':
            formatted_assembly = f'{assembly} assembly'
        filtered_phrase = None
        if filtered is True:
            filtered_phrase = 'filtered'
        elif filtered is False:
            filtered_phrase = 'unfiltered'
        software_version_phrase = None
        if analysis_step_version and predicted is not None:
            software_versions = set()
            asv_object = request.embed(analysis_step_version, '@@object?skip_calculated=true')
            for software_version in asv_object['software_versions']:
                software_version_object = request.embed(
                    software_version, '@@object_with_select_calculated_properties?field=summary')
                software_versions.add(software_version_object['summary'])
            software_version_phrase = f'({", ".join(sorted(software_versions))})'
        return ' '.join(
            [x for x in [formatted_assembly, transcriptome_annotation, predicted, filtered_phrase, content_type, software_version_phrase]
             if x is not None]
        )

    @calculated_property(schema={
        'title': 'Barcode Map For',
        'description': 'Link(s) to the Multiplexed samples using this file as barcode map.',
        'type': 'array',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Barcode Map For',
            'type': 'string',
            'linkFrom': 'MultiplexedSample.barcode_map',
        },
        'notSubmittable': True
    })
    def barcode_map_for(self, request, barcode_map_for):
        return paths_filtered_by_status(request, barcode_map_for)

    @calculated_property(schema={
        'title': 'Primer Design For',
        'description': 'Link(s) to the MeasurementSets using this file as a primer design.',
        'type': 'array',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Primer Design For',
            'type': 'string',
            'linkFrom': 'MeasurementSet.primer_designs',
        },
        'notSubmittable': True
    })
    def primer_design_for(self, request, primer_design_for):
        return paths_filtered_by_status(request, primer_design_for)


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

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'description': 'A summary of the image file.',
            'notSubmittable': True,
        }
    )
    def summary(self, content_type):
        return content_type


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

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'description': 'A summary of the model file.',
            'notSubmittable': True,
        }
    )
    def summary(self, content_type):
        return content_type


@collection(
    name='index-files',
    unique_key='accession',
    properties={
        'title': 'Index Files',
        'description': 'Listing of index files',
    }
)
class IndexFile(File):
    item_type = 'index_file'
    schema = load_schema('igvfd:schemas/index_file.json')
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
            'title': 'Summary',
            'type': 'string',
            'description': 'A summary of the index file.',
            'notSubmittable': True,
        }
    )
    def summary(self, content_type, derived_from):
        file_accessions = [x.split('/')[-2] for x in derived_from]
        derived_from_formatted = f" of {', '.join(file_accessions)}"
        return f'{content_type}{derived_from_formatted}'

    @calculated_property(
        schema={
            'title': 'Genome Assembly',
            'type': 'string',
            'description': 'The assembly associated with the index file.',
            'notSubmittable': True,
        }
    )
    def assembly(self, request, derived_from):
        parent_file_object = request.embed(derived_from[0], '@@object?skip_calculated=true')
        if 'assembly' in parent_file_object:
            return f'{parent_file_object["assembly"]}'

    @calculated_property(
        schema={
            'title': 'Transcriptome Annotation',
            'type': 'string',
            'description': 'The annotation and version of the reference resource.',
            'notSubmittable': True,
        }
    )
    def transcriptome_annotation(self, request, derived_from):
        parent_file_object = request.embed(derived_from[0], '@@object?skip_calculated=true')
        if 'transcriptome_annotation' in parent_file_object:
            return f'{parent_file_object["transcriptome_annotation"]}'

    @calculated_property(
        schema={
            'title': 'Filtered',
            'type': 'boolean',
            'description': 'Indicates whether reads that did not pass a filtering step, such as PCR duplicates, have been removed from the file.',
            'notSubmittable': True,
        }
    )
    def filtered(self, request, derived_from):
        parent_file_object = request.embed(derived_from[0], '@@object?skip_calculated=true')
        if 'filtered' in parent_file_object:
            return parent_file_object['filtered']

    @calculated_property(
        schema={
            'title': 'Redacted',
            'type': 'boolean',
            'description': 'Indicates whether the alignments data have been sanitized (redacted) to prevent leakage of private and potentially identifying genomic information.',
            'notSubmittable': True,
        }
    )
    def redacted(self, request, derived_from):
        parent_file_object = request.embed(derived_from[0], '@@object?skip_calculated=true')
        if 'redacted' in parent_file_object:
            return parent_file_object['redacted']


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
        # Allow download from prod bucket in sandbox/staging, as long as not restricted bucket.
        if 'restricted' in bucket:
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
    if properties['upload_status'] not in ['pending', 'file not found', 'invalidated']:
        raise HTTPForbidden(
            'Unable to issue new credentials when upload_status is validated or validation exempted'
        )
    if properties.get('status') not in ['in progress', 'preview']:
        raise HTTPForbidden(
            'Unable to issue new credentials when status is not in progress or preview'
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
    if properties.get('controlled_access') is True:
        if not request.has_permission('download_controlled_access_file'):
            raise HTTPForbidden(
                'Downloading controlled-access file not allowed.'
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
    raise HTTPTemporaryRedirect(
        location=location,
        headers=request.response.headers,  # Maintain any CORS headers set.
    )
