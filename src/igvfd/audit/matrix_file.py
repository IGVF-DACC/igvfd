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
    [
        {
            audit_description: Matrix files, with the exception of .hic files are expected to have different values for each dimension.,
            audit_category: identical dimensions,
            audit_level: WARNING
        }
    ]
    '''
    if value['dimension1'] == value['dimension2'] and value['file_format'] != 'hic':
        detail = (
            f'Matrix file {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'is expected to have different dimensions, but has '
            f'{value["dimension1"]} for both dimension 1 and dimension 2.'
        )
        yield AuditFailure('identical dimensions', detail, level='WARNING')
