from snovault import upgrade_step


@upgrade_step('modification', '1', '2')
def modification_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-729
    if 'cas' in value:
        print(value['cas'])
        print(value['cas_species'])
        #value['cas_species'] = 'Streptococcus pyogenes (Sp)'
    if 'schema_version' in value:
        print(value['schema_version'])
