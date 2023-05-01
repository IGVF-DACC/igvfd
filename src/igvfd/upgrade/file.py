from snovault import upgrade_step


@upgrade_step('reference_data', '1', '2')
@upgrade_step('sequence_data', '1', '2')
def file_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-398
    if 'accession' in value:
        accession_suffix = value['accession'][6:]
        value['accession'] = f'IGVFFI0{accession_suffix}A'


@upgrade_step('reference_data', '2', '3')
@upgrade_step('sequence_data', '2', '3')
def file_2_3(value, system):
    # https://igvf.atlassian.net/browse/IGVF-593
    return
