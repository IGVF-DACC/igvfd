from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('ConstructLibrarySet', frame='object')
def audit_construct_library_set_associated_phenotypes(value, system):
    '''
        audit_detail: Construct library sets with selection_criteria of phenotype-associated variants need to include an entry in associated_phenotypes.
        audit_category: inconsistent variants and phenotype metadata
        audit_levels: NOT_COMPLIANT
    '''
    detail = ''
    selection_criteria_list = value.get('selection_criteria', [])
    if 'phenotype-associated variants' in selection_criteria_list:
        assoc_pheno = value.get('associated_phenotypes', [])
        if assoc_pheno != []:
            return
        else:
            detail = (
                f'ConstructLibrarySet {audit_link(path_to_text(value["@id"]),value["@id"])} '
                f'has phenotype-associated variants listed in its selection_criteria, '
                f'but no phenotype term specified in associated_phenotypes.'
            )
            yield AuditFailure('inconsistent variants and phenotype metadata',
                               detail, level='NOT_COMPLIANT')


@audit_checker('ConstructLibrarySet', frame='object')
def audit_construct_library_set_plasmid_map(value, system):
    '''
        audit_detail: Construct library sets are expected to be associated with a plasmid map document.
        audit_category: missing plasmid
        audit_levels: WARNING
    '''
    map_counter = 0
    detail = (
        f'ConstructLibrarySet {audit_link(path_to_text(value["@id"]),value["@id"])} '
        f'does not have a plasmid map document attached.'
    )
    documents = value.get('documents', [])
    if documents == []:
        yield AuditFailure('missing plasmid map', detail, level='WARNING')
    else:
        for document in documents:
            document_obj = system.get('request').embed(document, '@@object?skip_calculated=true')
            if document_obj['document_type'] == 'plasmid map':
                map_counter += 1
                break
            else:
                continue
        if map_counter == 0:
            yield AuditFailure('missing plasmid map', detail, level='WARNING')


@audit_checker('ConstructLibrarySet', frame='object')
def audit_construct_library_set_scope(value, system):
    '''
        audit_detail: Construct library sets with a scope of tile or exon are expected to include only 1 element in the genes property.
        audit_category: inconsistent scope metadata
        audit_levels: WARNING
    '''
    detail = ''
    if value.get('scope') in ['exon', 'tile']:
        if len(value.get('small_scale_gene_list', [])) > 1:
            detail = (
                f'ConstructLibrarySet {audit_link(path_to_text(value["@id"]),value["@id"])} '
                f'specifies it has a scope of {value["scope"]}, but multiple genes are listed in the '
                f'small_scale_gene_list property.'
            )
            yield AuditFailure('inconsistent scope metadata',
                               detail, level='WARNING')


@audit_checker('ConstructLibrarySet', frame='object')
def audit_construct_library_set_files(value, system):
    '''
        audit_detail: Construct library sets are not expected to have any files except sequence files or configuration files.
        audit_category: unexpected file association
        audit_levels: WARNING
    '''
    non_sequence_files = []
    for file in value.get('files'):
        if not(file.startswith('/sequence-files/') or file.startswith('/configuration-files/')):
            non_sequence_files.append(file)
    if non_sequence_files:
        non_sequence_files = ', '.join(
            [audit_link(path_to_text(file), file) for file in non_sequence_files])
        detail = (f'ConstructLibrarySet {audit_link(path_to_text(value["@id"]),value["@id"])} links to '
                  f'file(s) that are not sequence or configuration files: {non_sequence_files}. This is unexpected as '
                  f'construct library sets are only expected to host sequence files or configuration files.')
        yield AuditFailure('unexpected file association', detail, level='WARNING')
