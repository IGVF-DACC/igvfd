from snovault import upgrade_step


@upgrade_step('human_donor', '1', '2')
@upgrade_step('rodent_donor', '1', '2')
def donor_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-221
    if 'parents' in value:
        if len(value['parents']) == 0:
            del value['parents']
    if 'external_resources' in value:
        if len(value['external_resources']) == 0:
            del value['external_resources']
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']
    if 'collections' in value:
        if len(value['collections']) == 0:
            del value['collections']
    if 'alternate_accessions' in value:
        if len(value['alternate_accessions']) == 0:
            del value['alternate_accessions']
    if 'documents' in value:
        if len(value['documents']) == 0:
            del value['documents']
    if 'references' in value:
        if len(value['references']) == 0:
            del value['references']


@upgrade_step('human_donor', '2', '3')
@upgrade_step('rodent_donor', '2', '3')
def donor_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-321
    if 'aliases' in value:
        value['alias'] = value['aliases']
        del value['aliases']
    if 'urls' in value:
        value['url'] = value['urls']
        del value['urls']
    if 'alternate_accessions' in value:
        value['alternate_accession'] = value['alternate_accessions']
        del value['alternate_accessions']
    if 'collections' in value:
        value['collection'] = value['collections']
        del value['collections']
    if 'documents' in value:
        value['document'] = value['documents']
        del value['documents']
    if 'references' in value:
        value['reference'] = value['references']
        del value['references']
    if 'traits' in value:
        value['traits'] = value['trait']
        del value['traits']
    if 'external_resources' in value:
        value['reference'] = value['external_resources']
        del value['external_resources']
