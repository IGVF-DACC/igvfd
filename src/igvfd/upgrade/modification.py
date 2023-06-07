from snovault import upgrade_step


@upgrade_step('modification', '1', '2')
def modification_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-729
    if 'cas_species' not in value:
        value['cas_species'] = 'Streptococcus pyogenes (Sp)'
