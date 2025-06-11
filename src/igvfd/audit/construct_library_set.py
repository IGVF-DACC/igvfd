from snovault.auditor import (
    AuditFailure,
    audit_checker
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message
)


def get_assay_terms(value, system):
    assay_terms = set()
    file_sets = value.get('file_sets', [])
    for file_set in file_sets:
        if file_set.startswith('/measurement-sets/'):
            file_set_object = system.get('request').embed(file_set, '@@object?skip_calculated=true')
            assay_terms.add(file_set_object['assay_term'])
    return list(assay_terms)


def audit_construct_library_set_associated_phenotypes(value, system):
    '''
    [
        {
            "audit_description": "Construct library sets with a selection criteria of phenotype-associated variants are expected to have associated phenotype(s).",
            "audit_category": "missing associated phenotypes",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    audit_message = get_audit_message(audit_construct_library_set_associated_phenotypes)
    detail = ''
    selection_criteria_list = value.get('selection_criteria', [])
    if 'phenotype-associated variants' in selection_criteria_list:
        assoc_pheno = value.get('associated_phenotypes', [])
        if assoc_pheno != []:
            return
        else:
            detail = (
                f'Construct library set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has phenotype-associated variants listed in its `selection_criteria`, '
                f'but no phenotype term specified in `associated_phenotypes`.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


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
    audit_message = get_audit_message(audit_construct_library_set_plasmid_map)
    map_counter = 0
    detail = (
        f'Construct library set {audit_link(path_to_text(value["@id"]), value["@id"])} '
        f'does not have a plasmid map attached in `documents`.'
    )
    documents = value.get('documents', [])
    if documents == []:
        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))
    else:
        for document in documents:
            document_obj = system.get('request').embed(document, '@@object?skip_calculated=true')
            if document_obj['document_type'] == 'plasmid map':
                map_counter += 1
                break
            else:
                continue
        if map_counter == 0:
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


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
    audit_message = get_audit_message(audit_construct_library_set_scope)
    detail = ''
    if value.get('scope') in ['exon', 'tile']:
        if len(value.get('small_scale_gene_list', [])) > 1:
            detail = (
                f'Construct library set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'specifies it has a `scope` of {value["scope"]}, but multiple genes are listed in '
                f'`small_scale_gene_list`.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''),
                               f'{detail} {audit_message.get("audit_description", "")})', level=audit_message.get('audit_level', ''))


def audit_integrated_content_files(value, system):
    '''
    [
        {
            "audit_description": "Guide libraries used in CRISPR assays are expected to link to an integrated content file of guide RNA sequences.",
            "audit_category": "missing guide RNA sequences",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "Reporter libraries used in MPRA assays are expected to link to an integrated content file of MPRA sequence designs.",
            "audit_category": "missing MPRA sequence designs",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    audit_message_guide = get_audit_message(audit_integrated_content_files, index=0)
    audit_message_reporter = get_audit_message(audit_integrated_content_files, index=1)
    assay_terms = get_assay_terms(value, system)
    CRISPR_assays = [
        '/assay-terms/OBI_0003659/',  # in vitro CRISPR screen assay
        '/assay-terms/OBI_0003660/',  # in vitro CRISPR screen using single-cell RNA-seq
        '/assay-terms/OBI_0003661/'  # in vitro CRISPR screen using flow cytometry
    ]
    MPRA_assays = [
        '/assay-terms/OBI_0002675/'  # massively parallel reporter assay
    ]
    library_expectation = {
        'guide library': ('guide RNA sequences', audit_message_guide, CRISPR_assays),
        'reporter library': ('MPRA sequence designs', audit_message_reporter, MPRA_assays),
    }
    integrated_content_files = value.get('integrated_content_files', '')
    library_type = value.get('file_set_type', '')
    if library_type in library_expectation and any(assay_term in library_expectation[library_type][2] for assay_term in assay_terms):
        file_expectation = library_expectation[library_type][0]
        audit_message = library_expectation[library_type][1]
        if integrated_content_files:
            files = [system.get('request').embed(file, '@@object?skip_calculated=true')
                     for file in integrated_content_files]
            if not ([file for file in files if file['content_type'] == file_expectation]):
                detail = (f'Construct library set {audit_link(path_to_text(value["@id"]), value["@id"])} has no '
                          f'linked files in `integrated_content_files` with `content_type` {file_expectation}.')
                yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))
        else:
            detail = (f'Construct library set {audit_link(path_to_text(value["@id"]), value["@id"])} has no '
                      f'`integrated_content_files`.')
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


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
    audit_message = get_audit_message(audit_construct_library_set_orf_gene)
    library_genes = set()
    orf_genes = set()
    if ('small_scale_gene_list' in value) and ('orf_list' in value):
        library_genes = set(value['small_scale_gene_list'])
        orf_ids = value.get('orf_list')
        for o in orf_ids:
            orf_object = system.get('request').embed(o + '@@object?skip_calculated=true')
            if 'genes' in orf_object:
                for d in orf_object['genes']:
                    orf_genes.add(d)

        if orf_genes != library_genes:
            detail = (
                f'Construct library set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has a `small_scale_gene_list` which does not match the genes of its associated `orf_list`.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


function_dispatcher_construct_library_set_object = {
    'audit_construct_library_set_associated_phenotypes': audit_construct_library_set_associated_phenotypes,
    'audit_construct_library_set_plasmid_map': audit_construct_library_set_plasmid_map,
    'audit_construct_library_set_scope': audit_construct_library_set_scope,
    'audit_integrated_content_files': audit_integrated_content_files,
    'audit_construct_library_set_orf_gene': audit_construct_library_set_orf_gene
}


@audit_checker('ConstructLibrarySet', frame='object')
def audit_construct_library_set_object_dispatcher(value, system):
    for function_name in function_dispatcher_construct_library_set_object.keys():
        for failure in function_dispatcher_construct_library_set_object[function_name](value, system):
            yield failure
