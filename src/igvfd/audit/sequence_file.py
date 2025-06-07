from snovault.auditor import (
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message,
    space_in_words,
)
from .audit_registry import register_audit, register_all_audits


@register_audit(['SequenceFile'], frame='object')
def audit_multiple_seqspec_per_seqfile(value, system):
    '''
    [
        {
            "audit_description": "A sequence file is expected to have only one released sequence specification file.",
            "audit_category": "unexpected seqspecs",
            "audit_level": "ERROR"
        },
        {
            "audit_description": "A sequence file is expected to have only one in progress sequence specification file.",
            "audit_category": "unexpected seqspecs",
            "audit_level": "INTERNAL_ACTION"
        }
    ]
    '''
    audit_msg_multi_released_seqspec = get_audit_message(audit_function=audit_multiple_seqspec_per_seqfile, index=0)
    audit_msg_multi_inprogress_seqspec = get_audit_message(audit_function=audit_multiple_seqspec_per_seqfile, index=1)
    seqspec_files = value.get('seqspecs', '')
    if len(seqspec_files) > 1:
        all_seqspec_file_status = []
        for seqspec_file in seqspec_files:
            seqspec_file_obj = system.get('request').embed(seqspec_file, '@@object?skip_calculated=true')
            seqspec_file_status = seqspec_file_obj.get('status', '')
            all_seqspec_file_status.append(seqspec_file_status)
        if all_seqspec_file_status.count('released') > 1:
            detail = (
                f'Sequence File {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has multiple released sequence specification files.'
            )
            yield AuditFailure(audit_msg_multi_released_seqspec.get('audit_category', ''), f'{detail} {audit_msg_multi_released_seqspec.get("audit_description", "")}', level=audit_msg_multi_released_seqspec.get('audit_level', ''))
        if all_seqspec_file_status.count('in progress') > 1:
            detail = (
                f'Sequence File {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has multiple in progress sequence specification files.'
            )
            yield AuditFailure(audit_msg_multi_inprogress_seqspec.get('audit_category', ''), f'{detail} {audit_msg_multi_inprogress_seqspec.get("audit_description", "")}', level=audit_msg_multi_inprogress_seqspec.get('audit_level', ''))


@register_audit(['SequenceFile'], frame='object')
def audit_external_identifiers(value, system):
    '''
    [
        {
            "audit_description": "Externally hosted files are expected to have identifiers from external resources in dbxrefs.",
            "audit_category": "missing dbxrefs",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    audit_message = get_audit_message(audit_external_identifiers)
    object_type = space_in_words(value['@type'][0]).capitalize()
    if value.get('externally_hosted'):
        if 'dbxrefs' not in value:
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} is externally hosted, '
                f'but does not have identifier(s) from an external resource listed in `dbxrefs`.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


register_all_audits()
