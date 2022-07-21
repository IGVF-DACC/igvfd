from snovault import upgrade_step


@upgrade_step('human_donor', '1', '2')
def human_donor_1_2(value, system):
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
