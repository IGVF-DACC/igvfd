from snovault import upgrade_step


@upgrade_step('whole_organism', '1', '2')
def whole_organism_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-207
    return
