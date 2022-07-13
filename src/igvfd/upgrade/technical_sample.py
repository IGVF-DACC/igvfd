from snovault import upgrade_step


@upgrade_step('technical_sample', '1', '2')
def technical_sample_1_2(value, system):
    if 'dbxrefs' in value:
        if len(value['dbxrefs']) == 0:
            del value['dbxrefs']
    if 'aliases' in value:
        if len(value['aliases']) == 0:
            del value['aliases']
    if 'alternate_accessions' in value:
        if len(value['alternate_accessions']) == 0:
            del value['alternate_accessions']
