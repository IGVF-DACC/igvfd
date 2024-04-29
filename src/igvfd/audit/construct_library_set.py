from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_description
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
                f'has phenotype-associated variants listed in its `selection_criteria`, '
                f'but no phenotype term specified in `associated_phenotypes`.'
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
        f'does not have a plasmid map attached in `documents`.'
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
                f'specifies it has a `scope` of {value["scope"]}, but multiple genes are listed in '
                f'`small_scale_gene_list`.'
            )
            yield AuditFailure('inconsistent scope',
                               f'{detail} {description}', level='WARNING')


@audit_checker('ConstructLibrarySet', frame='object')
def audit_construct_library_set_guide_design(value, system):
    '''
    [
        {
            "audit_description": "Guide libraries are expected to link to an integrated content file of guide RNA sequences.",
            "audit_category": "missing guide RNA sequences",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    description = get_audit_description(audit_construct_library_set_guide_design)
    if value.get('file_set_type', '') == 'guide library':
        integrated_content_files = value.get('integrated_content_files', '')
        if integrated_content_files:
            files = [system.get('request').embed(file, '@@object?skip_calculated=true')
                     for file in integrated_content_files]
            if not([file for file in files if file['content_type'] == 'guide RNA sequences']):
                detail = (f'Construct library set {audit_link(path_to_text(value["@id"]),value["@id"])} has no '
                          f'linked files in `integrated_content_files` with `content_type` "guide RNA sequences".')
                yield AuditFailure('missing guide RNA sequences', f'{detail} {description}', level='NOT_COMPLIANT')
        else:
            detail = (f'Construct library set {audit_link(path_to_text(value["@id"]),value["@id"])} has no '
                      f'`integrated_content_files`.')
            yield AuditFailure('missing guide RNA sequences', f'{detail} {description}', level='NOT_COMPLIANT')


@audit_checker('ConstructLibrarySet', frame='object')
def audit_construct_library_set_orf_gene(value, system):
    '''
    [
        {
            "audit_description": "Genes listed in the library are expected to match the open read frame gene.",
            "audit_category": "inconsistent genes",
            "audit_level": "ERROR"
        }
    ]
    '''
    description = get_audit_description(audit_construct_library_set_orf_gene)
    library_genes = set()
    orf_genes = set()
    if ('small_scale_gene_list' in value) and ('orf_list' in value):
        library_genes = set(value['small_scale_gene_list'])
        orf_ids = value.get('orf_list')
        for o in orf_ids:
            orf_object = system.get('request').embed(o + '@@object?skip_calculated=true')
            if 'gene' in orf_object:
                for d in orf_object['gene']:
                    orf_genes.add(d)

        if orf_genes != library_genes:
            detail = (
                f'Construct library set {audit_link(path_to_text(value["@id"]),value["@id"])} '
                f'has a `small_scale_gene_list` which does not match the genes of its associated `orf_list`.'
            )
            yield AuditFailure('inconsistent genes', f'{detail} {description}', level='ERROR')
