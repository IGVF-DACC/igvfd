from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_description
)


@audit_checker('MatrixFile', frame='object')
def audit_matrix_file_dimensions(value, system):
    '''
    [
        {
            "audit_description": "Matrix files, with the exception of .hic files are expected to have different values for each dimension.",
            "audit_category": "inconsistent dimensions",
            "audit_level": "WARNING"
        }
    ]
    '''
    description = get_audit_description(audit_matrix_file_dimensions)
    if value['dimension1'] == value['dimension2'] and value['file_format'] != 'hic':
        detail = (
            f'Matrix file {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has {value["dimension1"]} for both `dimension1` and `dimension2`.'
        )
        yield AuditFailure('inconsistent dimensions', f'{detail} {description}', level='WARNING')
