from snovault.auditor import (
    AuditFailure,
    audit_checker
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message,
    space_in_words
)


def audit_index_files_derived_from(value, system):
    '''
    [
        {
            "audit_description": "Index files in tbi format are expected to have a corresponding bed, tsv or vcf file in `derived_from`.",
            "audit_category": "unexpected indexed file",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message_tbi = get_audit_message(audit_index_files_derived_from)
    object_type = space_in_words(value['@type'][0]).capitalize()
    # For tbi files, check that the indexed file is of an expected file_format.
    # No need to check bai files, since Alignment Files can only be bams.
    derived_from_file = value.get('derived_from', [])
    derived_from_file_obj = system.get('request').embed(derived_from_file[0], '@@object?skip_calculated=true')
    if value['file_format'] == 'tbi':
        if derived_from_file_obj.get('file_format') not in ['tsv', 'vcf', 'bed']:
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has a file of unexpected file format in `derived_from`.')
            yield AuditFailure(
                audit_message_tbi.get('audit_category', ''),
                f'{detail} {audit_message_tbi.get("audit_description", "")}',
                level=audit_message_tbi.get('audit_level', '')
            )


function_dispatcher_index_file_object = {
    'audit_index_files_derived_from': audit_index_files_derived_from
}


@audit_checker('IndexFile', frame='object')
def audit_index_file_object_dispatcher(value, system):
    for function_name in function_dispatcher_index_file_object.keys():
        for failure in function_dispatcher_index_file_object[function_name](value, system):
            yield failure
