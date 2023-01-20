from snovault import upgrade_step


@upgrade_step('reference_data', '1', '2')
@upgrade_step('sequence_data', '1', '2')
def file_1_2(value, system):
    # https://igvf.atlassian.net/browse/IGVF-398
    if 'accession' in value:
        accession = value['accession']
        accession = accession.replace('FFF', 'FFI')
