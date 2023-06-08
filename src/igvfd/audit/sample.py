from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('Sample', frame='object?skip_calculated=true')
def audit_sample_sorted_fraction_parent_child_check(value, system):
    '''Samples that are a sorted_fraction of a parent sample should share
    most of the parent's metadata properties'''
    if 'sorted_fraction' in value:
        error_keys = []
        prop_errors = ''
        value_id = system.get('path')
        parent_id = value.get('sorted_fraction')
        parent = system.get('request').embed(parent_id + '@@object?skip_calculated=true')
        skip_keys = ['accession', 'alternate_accessions', 'aliases', 'audit', 'creation_timestamp', 'date_obtained',
                     'schema_version', 'starting_amount', 'starting_amount_units', 'submitted_by', 'description',
                     'sorted_fraction', 'sorted_fraction_detail', 'revoke_detail', 'notes', 'submitter_comment',
                     'documents', 'url', 'dbxrefs', 'pooled_from', 'part_of', 'originated_from']
        all_keys = parent.keys() | value.keys()
        keys_to_check = [k for k in all_keys if k not in skip_keys]
        for key in keys_to_check:
            if value.get(key, None) != parent.get(key, None):
                error_keys.append(key)
        prop_errors = ', '.join(error_keys)
        detail = (
            f'Sample {audit_link(path_to_text(value_id), value_id)} '
            f'has metadata ({prop_errors}) inconsistent with '
            f'its associated parent sample {audit_link(path_to_text(parent_id), parent_id)}.'
        )
        if prop_errors != '':
            yield AuditFailure('inconsistent sorted fraction metadata', detail, level='ERROR')


@audit_checker('Sample', frame='object?skip_calculated=true')
def audit_sample_virtual_donor_check(value, system):
    '''Non-virtual samples should not be linked to virtual donors.'''
    if 'virtual' and 'donors' in value:
        sample_virtual = value['virtual']
        donor_ids = value.get('donors')
        for d in donor_ids:
            donor_object = system.get('request').embed(d + '@@object?skip_calculated=true')
            donor_virtual = donor_object.get('virtual')
            if (sample_virtual == 'True') and (donor_virtual == 'True'):
                print('donor and sample both virtual')
            if (sample_virtual == 'True') and (donor_virtual == 'False'):
                print('Sample is virtual and donor is real...')
            if (sample_virtual == 'False') and (donor_virtual == 'True'):
                print('Sample is real and donor is virtual...')
                detail = ()
                yield AuditFailure('non-virtual sample linked to virtual donor', detail, level='ERROR')
            if (sample_virtual == 'False') and (donor_virtual == 'False'):
                print('Sample and donor are both real')
