from snovault.auditor import (
    AuditFailure,
    audit_checker
)

from snovault.mapping import watch_for_changes_in

from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message
)


def audit_workflow_without_asvs(value, system):
    '''
    [
        {
            "audit_description": "Workflows are expected to be associated with one or more analysis step version(s).",
            "audit_category": "missing analysis step versions",
            "audit_level": "WARNING"
        }
    ]
    '''
    # Audit 1: missing analysis step versions
    missing_asv_msg = get_audit_message(audit_workflow_without_asvs, index=0)
    if 'analysis_step_versions' not in value:
        detail = f'Workflow {audit_link(path_to_text(value["@id"]), value["@id"])} does not have any analysis step version.'
        yield AuditFailure(missing_asv_msg.get('audit_category', ''), f'{detail} {missing_asv_msg.get("audit_description", "")}', level=missing_asv_msg.get('audit_level', ''))


function_dispatcher_workflow_object = {
    'audit_workflow_without_asvs': audit_workflow_without_asvs
}


@audit_checker('Workflow', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_workflow_object.values()))
def audit_workflow_object_dispatcher(value, system):
    for function_name in function_dispatcher_workflow_object.keys():
        for failure in function_dispatcher_workflow_object[function_name](value, system):
            yield failure
