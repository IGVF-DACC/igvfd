from snovault import upgrade_step


@upgrade_step('tissue', '2', '3')
def tissue_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-210
    return


@upgrade_step('tissue', '1', '2')
def tissue_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-207
    return


@upgrade_step('tissue', '2', '3')
def tissue_2_3(value, system):
    if 'treatments' in value:
        if len(value['treatments']) == 0:
            del value['treatments']
    if 'donors' in value:
        if len(value['donors']) == 0:
            del value['donors']
    if 'dbxrefs' in value:
        if len(value['dbxrefs']) == 0:
            del value['dbxrefs']
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']
    if 'collections' in value:
        if len(value['collections']) == 0:
            del value['collections']
    if 'alternate_accessions' in value:
        if len(value['alternate_accessions']) == 0:
            del value['alternate_accessions']
