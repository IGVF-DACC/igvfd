from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_description
)
from .file_set import (
    find_non_config_sequence_files
)


@audit_checker('ConstructLibrarySet', frame='object')
def audit_construct_library_set_associated_phenotypes(value, system):
    '''
    [
        {
            "audit_description": "Construct library sets with a selection criteria of phenotype-associated variants are expected to have associated phenotype(s).",
            "audit_category": "missing associated phenotype",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    description = get_audit_description(audit_construct_library_set_associated_phenotypes)
    detail = ''
    selection_criteria_list = value.get('selection_criteria', [])
    if 'phenotype-associated variants' in selection_criteria_list:
        assoc_pheno = value.get('associated_phenotypes', [])
        if assoc_pheno != []:
            return
        else:
            detail = (
                f'Construct library set {audit_link(path_to_text(value["@id"]),value["@id"])} '
                f'has phenotype-associated variants listed in its selection_criteria, '
                f'but no phenotype term specified in associated_phenotypes.'
            )
            yield AuditFailure('missing associated phenotypes',
                               f'{detail} {description}', level='NOT_COMPLIANT')


@audit_checker('ConstructLibrarySet', frame='object')
def audit_construct_library_set_plasmid_map(value, system):
    '''
    [
        {
            "audit_description": "Construct library sets are expected to be associated with a plasmid map document.",
            "audit_category": "missing plasmid map",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    description = get_audit_description(audit_construct_library_set_plasmid_map)
    map_counter = 0
    detail = (
        f'Construct library set {audit_link(path_to_text(value["@id"]),value["@id"])} '
        f'does not have a plasmid map document attached.'
    )
    documents = value.get('documents', [])
    if documents == []:
        yield AuditFailure('missing plasmid map', f'{detail} {description}', level='NOT_COMPLIANT')
    else:
        for document in documents:
            document_obj = system.get('request').embed(document, '@@object?skip_calculated=true')
            if document_obj['document_type'] == 'plasmid map':
                map_counter += 1
                break
            else:
                continue
        if map_counter == 0:
            yield AuditFailure('missing plasmid map', f'{detail} {description}', level='NOT_COMPLIANT')


@audit_checker('ConstructLibrarySet', frame='object')
def audit_construct_library_set_scope(value, system):
    '''
    [
        {
            "audit_description": "Construct library sets with a scope of tile or exon are expected to only link to one gene.",
            "audit_category": "inconsistent scope",
            "audit_level": "WARNING"
        }
    ]
    '''
    description = get_audit_description(audit_construct_library_set_scope)
    detail = ''
    if value.get('scope') in ['exon', 'tile']:
        if len(value.get('small_scale_gene_list', [])) > 1:
            detail = (
                f'Construct library set {audit_link(path_to_text(value["@id"]),value["@id"])} '
                f'specifies it has a scope of {value["scope"]}, but multiple genes are listed in the '
                f'small_scale_gene_list property.'
            )
            yield AuditFailure('inconsistent scope',
                               f'{detail} {description}', level='WARNING')


@audit_checker('ConstructLibrarySet', frame='object')
def audit_construct_library_set_files(value, system):
    '''
    [
        {
            "audit_description": "Construct library sets are expected to contain only sequence files or configuration files.",
            "audit_category": "unexpected files",
            "audit_level": "WARNING"
        }
    ]
    '''
    description = get_audit_description(audit_construct_library_set_files)
    non_sequence_files = find_non_config_sequence_files(value)
    if non_sequence_files:
        non_sequence_files = ', '.join(
            [audit_link(path_to_text(file), file) for file in non_sequence_files])
        detail = (f'Construct library set {audit_link(path_to_text(value["@id"]),value["@id"])} links to '
                  f'file(s) that are not sequence or configuration files: {non_sequence_files}.')
        yield AuditFailure('unexpected files', f'{detail} {description}', level='WARNING')
