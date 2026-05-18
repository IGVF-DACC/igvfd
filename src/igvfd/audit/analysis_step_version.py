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


def audit_analysis_step_version_missing_workflows(value, system):
    '''
    [
        {
            "audit_description": "Analysis step versions should be associated with at least one workflow.",
            "audit_category": "missing workflows",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    audit_message = get_audit_message(audit_analysis_step_version_missing_workflows, index=0)
    if not value.get('workflows', []):
        detail = (
            f'Analysis step version {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has no associated workflows.'
        )
        yield AuditFailure(
            audit_message.get('audit_category', ''),
            f'{detail} {audit_message.get("audit_description", "")}',
            level=audit_message.get('audit_level', '')
        )


function_dispatcher_analysis_step_version_object = {
    'audit_analysis_step_version_missing_workflows': audit_analysis_step_version_missing_workflows,
}


@audit_checker('AnalysisStepVersion', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_analysis_step_version_object.values()))
def audit_analysis_step_version_object_dispatcher(value, system):
    for function_name in function_dispatcher_analysis_step_version_object.keys():
        for failure in function_dispatcher_analysis_step_version_object[function_name](value, system):
            yield failure
