from snovault.auditor import (
    AuditFailure,
    audit_checker
)

from snovault.mapping import watch_for_changes_in

from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message,
    space_in_words
)


def audit_upload_status(value, system):
    '''
    [
        {
            "audit_description": "Files are expected to be validated or validation exempted.",
            "audit_category": "upload status not validated",
            "audit_level": "ERROR"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    upload_status = value.get('upload_status')
    if upload_status not in ['validated', 'validation exempted'] and not (value.get('externally_hosted', False)):
        # If a file in validated and not externally hosted, it should be an ERROR.
        audit_message = get_audit_message(audit_upload_status, index=0)
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has `upload_status` {upload_status}.'
        )
        validation_error_detail = value.get('validation_error_detail')
        if upload_status == 'invalidated' and validation_error_detail:
            detail = f'{detail} Validation error detail: {validation_error_detail}.'
        yield AuditFailure(
            'upload status not validated',
            f'{detail} {audit_message.get("audit_description", "")}',
            level=audit_message.get('audit_level')
        )


def audit_file_format_specifications(value, system):
    '''
    [
        {
            "audit_description": "File format specifications are excepted to be documents have type file format specification.",
            "audit_category": "inconsistent document type",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message = get_audit_message(audit_file_format_specifications)
    object_type = space_in_words(value['@type'][0]).capitalize()
    for document in value.get('file_format_specifications', []):
        document_object = system.get('request').embed(document)
        doc_type = document_object['document_type']
        if doc_type != 'file format specification':
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has `file_format_specification` {audit_link(path_to_text(document), document)} '
                f'with `document_type` {doc_type}.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


def audit_file_no_file_format_specifications(value, system):
    '''
    [
        {
            "audit_description": "Tabular files, with the exception of vcf files, are expected to link to a file format specifications document describing the headers of the file.",
            "audit_category": "missing file format specifications",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "Matrix files are expected to link to a file format specifications document describing the axes and layers of the file.",
            "audit_category": "missing file format specifications",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "Model files in tsv format are expected to link to a file format specifications document describing the content of the file.",
            "audit_category": "missing file format specifications",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    if object_type == 'Tabular file':
        if value.get('file_format') == 'vcf':
            return
        audit_message = get_audit_message(audit_file_no_file_format_specifications, index=0)
    elif object_type == 'Matrix file':
        audit_message = get_audit_message(audit_file_no_file_format_specifications, index=1)
    elif object_type == 'Model file':
        if value.get('file_format') != 'tsv':
            return
        audit_message = get_audit_message(audit_file_no_file_format_specifications, index=2)
    if not (value.get('file_format_specifications')):
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has no `file_format_specifications`.'
        )
        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


def audit_file_mixed_assembly_transcriptome_annotation(value, system):
    '''
    [
        {
            "audit_description": "Files are expected to have a transcriptome annotation consistent with its assembly.",
            "audit_category": "inconsistent transcriptome annotation",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "Files are expected to have only 1 transcriptome annotation.",
            "audit_category": "mixed transcriptome annotation",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "Files are expected to have only 1 assembly.",
            "audit_category": "mixed assembly",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message_inconsistent_annotation = get_audit_message(
        audit_file_mixed_assembly_transcriptome_annotation, index=0)
    audit_message_mixed_annotation = get_audit_message(audit_file_mixed_assembly_transcriptome_annotation, index=1)
    audit_message_mixed_assembly = get_audit_message(audit_file_mixed_assembly_transcriptome_annotation, index=2)
    assembly_to_annotation = {
        'GRCm39': [
            'GENCODE M30',
            'GENCODE M31',
            'GENCODE M32',
            'GENCODE M33',
            'GENCODE M34',
            'GENCODE M36'
        ],
        'mm10': [
            'GENCODE M25',
            'GENCODE M17'
        ],
        'Cast - GRCm39': [
            'GENCODE Cast - M32'
        ],
        'GRCh38': [
            'GENCODE 22',
            'GENCODE 24',
            'GENCODE 28',
            'GENCODE 32',
            'GENCODE 40',
            'GENCODE 41',
            'GENCODE 42',
            'GENCODE 43',
            'GENCODE 44',
            'GENCODE 45',
            'GENCODE 47'
        ],
        'GRCh38, mm10': [
            'GENCODE 32, GENCODE M23'
        ],
        'Mixed genome assemblies': [],
        'custom': []
    }
    if value.get('transcriptome_annotation', '') and value.get('assembly', '') and \
            value.get('transcriptome_annotation', '') != 'Mixed transcriptome annotations' and \
            value.get('assembly', '') != 'Mixed genome assemblies' and \
            value.get('transcriptome_annotation', '') not in assembly_to_annotation[value.get('assembly', '')]:
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has a `transcriptome_annotation` {value.get("transcriptome_annotation", "")} '
            f'that is inconsistent with its assembly {value.get("assembly", "")}.'
        )
        yield AuditFailure(audit_message_inconsistent_annotation.get('audit_category', ''), f'{detail} {audit_message_inconsistent_annotation.get("audit_description", "")}', level=audit_message_inconsistent_annotation.get('audit_level', ''))

    if value.get('transcriptome_annotation', '') == 'Mixed transcriptome annotations':
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has mixed transcriptome annotations.'
        )
        yield AuditFailure(audit_message_mixed_annotation.get('audit_category', ''), f'{detail} {audit_message_mixed_annotation.get("audit_description", "")}', level=audit_message_mixed_annotation.get('audit_level', ''))

    if value.get('assembly', '') == 'Mixed genome assemblies':
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has mixed assemblies.'
        )
        yield AuditFailure(audit_message_mixed_assembly.get('audit_category', ''), f'{detail} {audit_message_mixed_assembly.get("audit_description", "")}', level=audit_message_mixed_assembly.get('audit_level', ''))


def audit_file_in_correct_bucket(value, system):
    request = system.get('request')
    file_item = request.root.get_by_uuid(value['uuid'])
    result, current_path, destination_path = file_item._file_in_correct_bucket(request)
    if not result:
        detail = ('Move {} file {} from {} to {}'.format(
            value.get('status'),
            value.get('accession', value.get('uuid')),
            current_path,
            destination_path
        )
        )
        yield AuditFailure(
            'incorrect file bucket',
            detail,
            level='INTERNAL_ACTION'
        )


function_dispatcher_file_object = {
    'audit_upload_status': audit_upload_status,
    'audit_file_format_specifications': audit_file_format_specifications,
    'audit_file_in_correct_bucket': audit_file_in_correct_bucket,
}

function_dispatcher_alignment_file_object = {
    'audit_file_mixed_assembly_transcriptome_annotation': audit_file_mixed_assembly_transcriptome_annotation
}

function_dispatcher_matrix_file_object = {
    'audit_file_no_file_format_specifications': audit_file_no_file_format_specifications,
    'audit_file_mixed_assembly_transcriptome_annotation': audit_file_mixed_assembly_transcriptome_annotation
}

function_dispatcher_signal_file_object = {
    'audit_file_mixed_assembly_transcriptome_annotation': audit_file_mixed_assembly_transcriptome_annotation
}

function_dispatcher_tabular_file_object = {
    'audit_file_no_file_format_specifications': audit_file_no_file_format_specifications
}

function_dispatcher_model_file_object = {
    'audit_file_no_file_format_specifications': audit_file_no_file_format_specifications
}


@audit_checker('File', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_file_object.values()))
def audit_file_object_dispatcher(value, system):
    for function_name in function_dispatcher_file_object.keys():
        for failure in function_dispatcher_file_object[function_name](value, system):
            yield failure


@audit_checker('AlignmentFile', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_matrix_file_object.values()))
def audit_alignment_file_object_dispatcher(value, system):
    for function_name in function_dispatcher_alignment_file_object.keys():
        for failure in function_dispatcher_alignment_file_object[function_name](value, system):
            yield failure


@audit_checker('MatrixFile', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_matrix_file_object.values()))
def audit_matrix_file_object_dispatcher(value, system):
    for function_name in function_dispatcher_matrix_file_object.keys():
        for failure in function_dispatcher_matrix_file_object[function_name](value, system):
            yield failure


@audit_checker('SignalFile', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_matrix_file_object.values()))
def audit_signal_file_object_dispatcher(value, system):
    for function_name in function_dispatcher_signal_file_object.keys():
        for failure in function_dispatcher_signal_file_object[function_name](value, system):
            yield failure


@audit_checker('TabularFile', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_tabular_file_object.values()))
def audit_tabular_file_object_dispatcher(value, system):
    for function_name in function_dispatcher_tabular_file_object.keys():
        for failure in function_dispatcher_tabular_file_object[function_name](value, system):
            yield failure


@audit_checker('ModelFile', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_model_file_object.values()))
def audit_model_file_object_dispatcher(value, system):
    for function_name in function_dispatcher_model_file_object.keys():
        for failure in function_dispatcher_model_file_object[function_name](value, system):
            yield failure
