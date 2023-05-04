from snovault import upgrade_step


@upgrade_step('gene', '1', '2')
def gene_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-221
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']


@upgrade_step('gene', '2', '3')
def gene_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-268
    no_ensembl = []
    if 'ncbi_entrez_status' in value:
        del value['ncbi_entrez_status']
    if 'dbxrefs' in value:
        for dbxref in value['dbxrefs']:
            if dbxref.startswith('ENSEMBL:') == True:
                dbxref = dbxref.removeprefix('ENSEMBL:')
                value['geneid'] = dbxref
            else:
                no_ensembl.append(dbxref)
    value['dbxrefs'] = no_ensembl


@upgrade_step('gene', '3', '4')
def gene_3_4(value, system):
    # https://igvf.atlassian.net/browse/IGVF-629
    if value['taxa'] == 'Homo sapiens':
        value['annotation_version'] = 'GENCODE v42'
    if value['taxa'] == 'Mus musculus':
        value['annotation_version'] = 'GENCODE vM30'

    (geneid_new, version_number) = value['geneid'].split('.')
    value['geneid'] = geneid_new
    value['version_number'] = version_number
