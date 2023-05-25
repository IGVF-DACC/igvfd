from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('Biosample', frame='object')
def audit_biosample_nih_institutional_certification(value, system):
    '''
    Check if Biosample objects specify an NIH Institutional Certification which is required for human data.

    The function is meant to audit the 'Biosample' objects in the system, verifying that each Biosample
    intended for human data has an associated NIH Institutional Certification. If a Biosample object is
    associated with a human donor but does not specify a NIH Institutional Certification, it raises an audit
    failure.

    Args:
        value (dict): The Biosample object to be audited.
        system (any): System specific parameters.

    Yields:
        AuditFailure: An AuditFailure object specifying the Biosample object that fails the check.
    '''
    if ('nih_institutional_certification' not in value) and (any(donor.startswith('/human-donors/') for donor in value.get('donors'))):
        sample_id = value.get('@id')
        detail = (
            f'Biosample {audit_link(path_to_text(sample_id), sample_id)} '
            f'is missing NIH institutional certificate that is required for human samples.'
        )
        yield AuditFailure('missing nih_institutional_certification', detail, level='ERROR')


@audit_checker('Biosample', frame='object')
def audit_biosample_taxa_check(value, system):
    '''
    Audit function to flag biosamples associated with donors of different taxa.

    This function audits 'Biosample' objects in the system to verify that all donors associated with a
    Biosample object belong to the same taxa. If a Biosample is associated with donors from more than
    one taxa, it raises an audit failure.

    Args:
        value (dict): The Biosample object to be audited.
        system (any): System specific parameters.

    Yields:
        AuditFailure: An AuditFailure object specifying the Biosample object that fails the check.
    '''
    if 'donors' in value:
        sample_id = value['@id']
        donor_ids = value.get('donors')
        taxa_dict = {}
        for d in donor_ids:
            donor_object = system.get('request').embed(d + '@@object?skip_calculated=true')
            if donor_object.get('taxa'):
                taxa = donor_object.get('taxa')
                if taxa not in taxa_dict:
                    taxa_dict[taxa] = []

                taxa_dict[taxa].append(d)

        if len(taxa_dict) > 1:
            detail = ''
            for k, v in taxa_dict.items():
                detail += f'Biosample {audit_link(sample_id, sample_id)} has donors {audit_link(v, v)} that are {k}. '
            yield AuditFailure('inconsistent donor taxa', detail, level='ERROR')
