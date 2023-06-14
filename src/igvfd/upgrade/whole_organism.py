from snovault import upgrade_step


@upgrade_step('whole_organism', '13', '14')
def whole_organism_13_14(value, system):
    # https://igvf.atlassian.net/browse/IGVF-753
    if 'part_of' in value:
        del value['part_of']
    if 'pooled_from' in value:
        del value['pooled_from']
