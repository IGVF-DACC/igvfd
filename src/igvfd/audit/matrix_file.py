from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('MatrixFile', frame='object')
def audit_matrix_file_dimensions(value, system):
    '''
        audit_detail: Matrix files are expected to have different values for each dimension.
        audit_category: inconsistent dimensions
        audit_levels: WARNING
    '''
    if value['dimension1'] == value['dimension2']:
        detail = (
            f'Matrix file {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'is expected to have different values for each dimension.'
        )
        yield AuditFailure('inconsistent dimensions', detail, level='WARNING')
