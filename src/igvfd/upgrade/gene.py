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
    # https://igvf.atlassian.net/browse/IGVF-321
    if 'aliases' in value:
        value['alias'] = value['aliases']
        del value['aliases']
    if 'synonyms' in value:
        value['synonym'] = value['synonyms']
        del value['synonyms']
    if 'locations' in value:
        value['location'] = value['locations']
        del value['locations']
    if 'dbxrefs' in value:
        value['dbxref'] = value['dbxrefs']
        del value['dbxrefs']
