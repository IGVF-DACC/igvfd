from snovault import upgrade_step


@upgrade_step('whole_organism', '1', '2')
def whole_organism_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-207
    return

@upgrade_step('whole_organism', '2', '3')
def whole_organism_2_3(value, system):
    if 'treatments' in value and len(value['treatments']) == 0:
        del value['treatments']
    if 'donors' in value and len(value['donors']) == 0:
        del value['donors']
    if 'dbxrefs' in value and len(value['dbxrefs']) == 0:
        del value['dbxrefs']
